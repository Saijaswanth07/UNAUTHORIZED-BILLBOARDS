from datetime import datetime, timedelta
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
from .. import models, schemas
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)

class IncentiveService:
    """Service for managing user incentives and gamification"""
    
    # Points configuration
    POINTS = {
        'report_submitted': 10,
        'report_verified': 20,
        'violation_found': 30,
        'streak_bonus': 5,  # per day in streak
        'weekly_challenge': 50,
        'referral': 25,
    }
    
    # Reward tiers
    REWARD_TIERS = [
        {
            'name': 'Citizen',
            'points_required': 0,
            'benefits': ['Basic access', 'View reports']
        },
        {
            'name': 'Enforcer',
            'points_required': 100,
            'benefits': ['Priority support', 'Advanced analytics']
        },
        {
            'name': 'Champion',
            'points_required': 500,
            'benefits': ['Exclusive events', 'Beta features']
        },
        {
            'name': 'Legend',
            'points_required': 2000,
            'benefits': ['Meet the team', 'Special recognition']
        }
    ]
    
    def __init__(self, db: Session):
        self.db = db
    
    async def award_points(self, user_id: str, action: str, metadata: Optional[Dict] = None) -> int:
        """Award points to a user for an action"""
        if action not in self.POINTS:
            logger.warning(f"Unknown action for points: {action}")
            return 0
            
        points = self.POINTS[action]
        
        # Check for streak bonus
        if action == 'report_submitted':
            streak = await self._check_streak(user_id)
            if streak > 1:  # Only award bonus after first day
                points += streak * self.POINTS['streak_bonus']
        
        # Create point record
        point_record = models.UserPoints(
            user_id=user_id,
            points=points,
            action=action,
            metadata=metadata or {}
        )
        self.db.add(point_record)
        self.db.commit()
        
        # Update user's total points
        user = self.db.query(models.User).filter(models.User.id == user_id).first()
        if user:
            user.total_points = (user.total_points or 0) + points
            self.db.commit()
        
        return points
    
    async def _check_streak(self, user_id: str) -> int:
        """Check and update user's reporting streak"""
        # Get last report date
        last_report = self.db.query(models.UserPoints).filter(
            models.UserPoints.user_id == user_id,
            models.UserPoints.action == 'report_submitted'
        ).order_by(models.UserPoints.created_at.desc()).first()
        
        if not last_report:
            return 1  # First report
            
        # Check if last report was yesterday (within 36 hours to be lenient)
        time_since_last = datetime.utcnow() - last_report.created_at
        if time_since_last < timedelta(hours=36):
            # Already got points for today
            return 0
            
        # Check if we should continue streak (within 48 hours)
        if time_since_last < timedelta(hours=48):
            user = self.db.query(models.User).filter(models.User.id == user_id).first()
            if user:
                user.streak_days = (user.streak_days or 0) + 1
                self.db.commit()
                return user.streak_days
        
        # Reset streak if more than 48 hours
        user = self.db.query(models.User).filter(models.User.id == user_id).first()
        if user:
            user.streak_days = 1
            self.db.commit()
        return 1
    
    async def get_leaderboard(self, limit: int = 100) -> List[schemas.LeaderboardUser]:
        """Get leaderboard of top users"""
        # Get users with their report counts and points
        users = self.db.query(
            models.User.id,
            models.User.username,
            models.User.total_points,
            models.func.count(models.Report.id).label('report_count')
        ).outerjoin(
            models.Report,
            models.User.id == models.Report.user_id
        ).group_by(
            models.User.id
        ).order_by(
            models.User.total_points.desc()
        ).limit(limit).all()
        
        # Convert to leaderboard format
        leaderboard = []
        for rank, user in enumerate(users, 1):
            leaderboard.append(schemas.LeaderboardUser(
                user_id=user.id,
                username=user.username,
                score=user.total_points or 0,
                reports=user.report_count or 0,
                rank=rank
            ))
            
        return leaderboard
    
    async def get_user_rewards(self, user_id: str) -> Dict:
        """Get user's rewards and progress"""
        user = self.db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            return {}
            
        current_points = user.total_points or 0
        current_tier = self._get_tier_for_points(current_points)
        next_tier = self.REWARD_TIERS[current_tier['index'] + 1] if current_tier['index'] < len(self.REWARD_TIERS) - 1 else None
        
        return {
            'current_tier': current_tier,
            'next_tier': next_tier,
            'points_to_next': next_tier['points_required'] - current_points if next_tier else 0,
            'current_points': current_points,
            'streak_days': user.streak_days or 0
        }
    
    def _get_tier_for_points(self, points: int) -> Dict:
        """Get the tier for a given number of points"""
        tier = {
            'name': 'Citizen',
            'points_required': 0,
            'benefits': [],
            'index': 0
        }
        
        for idx, t in enumerate(self.REWARD_TIERS):
            if points >= t['points_required']:
                tier = {**t, 'index': idx}
            else:
                break
                
        return tier
    
    async def create_weekly_challenge(self):
        """Create weekly challenges for users"""
        # This would be called by a scheduled task
        # Implementation would create challenge records and notify users
        pass
    
    async def check_challenge_progress(self, user_id: str):
        """Check user's progress on current challenges"""
        # Implementation would check user's progress and award points
        pass
