import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  LinearProgress, 
  Grid, 
  Card, 
  CardContent, 
  Divider,
  Badge,
  Tooltip,
  Button
} from '@mui/material';
import { styled } from '@mui/material/styles';
import { publicApi, userApi } from '../../services/api';

const RewardTier = styled(Paper)(({ theme, active, achieved }) => ({
  padding: theme.spacing(3),
  textAlign: 'center',
  position: 'relative',
  transition: 'all 0.3s ease',
  border: active ? `2px solid ${theme.palette.primary.main}` : '1px solid rgba(0,0,0,0.12)',
  backgroundColor: achieved ? theme.palette.primary.light : theme.palette.background.paper,
  color: achieved ? theme.palette.primary.contrastText : 'inherit',
  '&:hover': {
    transform: 'translateY(-4px)',
    boxShadow: theme.shadows[4],
  },
}));

const ProgressBar = styled(Box)(({ theme }) => ({
  width: '100%',
  height: 20,
  backgroundColor: theme.palette.grey[200],
  borderRadius: 10,
  overflow: 'hidden',
  margin: theme.spacing(2, 0),
  position: 'relative',
}));

const ProgressFill = styled(Box)(({ progress }) => ({
  height: '100%',
  width: `${progress}%`,
  background: 'linear-gradient(90deg, #4CAF50, #8BC34A)',
  borderRadius: 'inherit',
  transition: 'width 0.5s ease-in-out',
}));

const BadgeIcon = styled(Box)(({ theme, color = 'primary' }) => ({
  width: 40,
  height: 40,
  borderRadius: '50%',
  backgroundColor: theme.palette[color].main,
  color: theme.palette[color].contrastText,
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'center',
  margin: '0 auto 16px',
  fontSize: '1.2rem',
  boxShadow: theme.shadows[2],
}));

const Rewards = () => {
  const [rewards, setRewards] = useState(null);
  const [tiers, setTiers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTier, setActiveTier] = useState(0);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        // In a real app, you would fetch this from your API
        const tiersData = await publicApi.fetchRewardTiers();
        setTiers(tiersData);
        
        const userRewards = await userApi.getUserRewards();
        setRewards(userRewards);
        
        // Find the current tier index
        const currentTierIndex = tiersData.findIndex(
          (tier, index) => 
            userRewards.current_points >= tier.points_required && 
            (index === tiersData.length - 1 || userRewards.current_points < tiersData[index + 1]?.points_required)
        );
        
        setActiveTier(Math.max(0, currentTierIndex));
      } catch (error) {
        console.error('Error fetching rewards data:', error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, []);

  if (loading) {
    return (
      <Box p={3}>
        <Typography>Loading rewards...</Typography>
      </Box>
    );
  }

  // Calculate progress to next tier
  const calculateProgress = () => {
    if (!rewards || !tiers.length) return 0;
    
    const currentTier = tiers[activeTier];
    const nextTier = tiers[activeTier + 1];
    
    if (!nextTier) return 100; // At max tier
    
    const pointsInCurrentTier = rewards.current_points - currentTier.points_required;
    const pointsNeededForNextTier = nextTier.points_required - currentTier.points_required;
    
    return Math.min(100, Math.round((pointsInCurrentTier / pointsNeededForNextTier) * 100));
  };

  const progress = calculateProgress();
  const currentTier = tiers[activeTier] || {};
  const nextTier = tiers[activeTier + 1] || null;
  const pointsToNextTier = nextTier ? nextTier.points_required - rewards.current_points : 0;

  return (
    <Box p={3}>
      <Typography variant="h4" gutterBottom>
        Your Rewards
      </Typography>
      
      {/* Current Tier Status */}
      <Paper sx={{ p: 3, mb: 4, bgcolor: 'primary.light', color: 'primary.contrastText' }}>
        <Grid container spacing={3} alignItems="center">
          <Grid item xs={12} md={4} textAlign="center">
            <Typography variant="h6">Current Tier</Typography>
            <Typography variant="h3" fontWeight="bold">
              {currentTier?.name || 'Citizen'}
            </Typography>
          </Grid>
          
          <Grid item xs={12} md={4} textAlign="center">
            <Typography variant="h6">Your Points</Typography>
            <Typography variant="h3" fontWeight="bold">
              {rewards?.current_points || 0}
            </Typography>
          </Grid>
          
          <Grid item xs={12} md={4} textAlign="center">
            <Typography variant="h6">
              {nextTier ? `Next Tier: ${nextTier.name}` : 'Highest Tier Achieved!'}
            </Typography>
            {nextTier ? (
              <Typography variant="h6">
                {pointsToNextTier} more points to go
              </Typography>
            ) : (
              <Typography variant="h6">You've reached the top!</Typography>
            )}
          </Grid>
        </Grid>
        
        {nextTier && (
          <Box mt={2}>
            <Box display="flex" justifyContent="space-between" mb={1}>
              <Typography variant="body2">
                {currentTier?.name} ({rewards?.current_points} pts)
              </Typography>
              <Typography variant="body2">
                {nextTier?.name} ({nextTier?.points_required} pts)
              </Typography>
            </Box>
            <ProgressBar>
              <ProgressFill progress={progress} />
            </ProgressBar>
            <Typography variant="caption" display="block" textAlign="center">
              {progress}% to next tier
            </Typography>
          </Box>
        )}
      </Paper>
      
      {/* Tier Benefits */}
      <Typography variant="h5" gutterBottom>
        Tier Benefits
      </Typography>
      
      <Grid container spacing={3} mb={4}>
        {tiers.map((tier, index) => (
          <Grid item xs={12} sm={6} md={3} key={tier.name}>
            <RewardTier 
              active={index === activeTier}
              achieved={index <= activeTier}
              onClick={() => setActiveTier(index)}
            >
              {index <= activeTier && (
                <Badge
                  badgeContent="✓"
                  color="success"
                  sx={{
                    position: 'absolute',
                    top: 8,
                    right: 8,
                    '& .MuiBadge-badge': {
                      width: 24,
                      height: 24,
                      borderRadius: '50%',
                      backgroundColor: 'success.main',
                      color: 'success.contrastText',
                    },
                  }}
                >
                  <Box />
                </Badge>
              )}
              
              <BadgeIcon color={index <= activeTier ? 'primary' : 'grey'}>
                {tier.icon || tier.name.charAt(0)}
              </BadgeIcon>
              
              <Typography variant="h6" gutterBottom>
                {tier.name}
              </Typography>
              
              <Typography variant="body2" color="textSecondary" gutterBottom>
                {tier.points_required} points
              </Typography>
              
              <Divider sx={{ my: 2 }} />
              
              <Box textAlign="left">
                <Typography variant="subtitle2" gutterBottom>
                  Benefits:
                </Typography>
                <ul style={{ paddingLeft: 20, margin: 0 }}>
                  {tier.benefits.map((benefit, i) => (
                    <li key={i}>
                      <Typography variant="body2">{benefit}</Typography>
                    </li>
                  ))}
                </ul>
              </Box>
              
              {index === activeTier && (
                <Box mt={2}>
                  <Button 
                    variant="contained" 
                    color="primary"
                    fullWidth
                    disabled={!nextTier}
                  >
                    {nextTier ? `Earn ${pointsToNextTier} more points` : 'Top Tier Achieved!'}
                  </Button>
                </Box>
              )}
            </RewardTier>
          </Grid>
        ))}
      </Grid>
      
      {/* Available Rewards */}
      <Typography variant="h5" gutterBottom>
        Available Rewards
      </Typography>
      
      <Grid container spacing={3} mb={4}>
        {rewards?.available_rewards?.map((reward, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <Card>
              <CardContent>
                <Box display="flex" alignItems="center" mb={2}>
                  <BadgeIcon color={reward.affordable ? 'primary' : 'grey'}>
                    {reward.icon || '🎁'}
                  </BadgeIcon>
                  <Box ml={2}>
                    <Typography variant="h6">{reward.name}</Typography>
                    <Typography variant="body2" color="textSecondary">
                      {reward.points_required} points
                    </Typography>
                  </Box>
                </Box>
                
                <Typography variant="body2" paragraph>
                  {reward.description}
                </Typography>
                
                <Button 
                  variant={reward.affordable ? 'contained' : 'outlined'}
                  color="primary"
                  fullWidth
                  disabled={!reward.affordable}
                >
                  {reward.affordable ? 'Claim Reward' : `Need ${reward.points_required - rewards.current_points} more points`}
                </Button>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
      
      {/* How to Earn More Points */}
      <Paper sx={{ p: 3, mb: 4 }}>
        <Typography variant="h5" gutterBottom>
          How to Earn More Points
        </Typography>
        
        <Grid container spacing={2}>
          {[
            { action: 'Submit a Report', points: '+10', description: 'Earn points for each valid report submitted' },
            { action: 'Report Verified', points: '+20', description: 'When your report is verified by our team' },
            { action: 'Daily Login', points: '+5', description: 'Log in daily to maintain your streak' },
            { action: 'Weekly Challenge', points: '+50', description: 'Complete weekly reporting challenges' },
            { action: 'Refer a Friend', points: '+25', description: 'When your friend signs up and submits a report' },
            { action: 'Top Contributor', points: '+100', description: 'Be among the top 10 reporters of the month' },
          ].map((item, index) => (
            <Grid item xs={12} sm={6} md={4} key={index}>
              <Box display="flex" alignItems="flex-start">
                <Box 
                  sx={{
                    bgcolor: 'primary.main',
                    color: 'primary.contrastText',
                    borderRadius: '4px',
                    p: 1,
                    minWidth: 50,
                    textAlign: 'center',
                    mr: 2,
                  }}
                >
                  <Typography variant="subtitle2" fontWeight="bold">
                    {item.points}
                  </Typography>
                </Box>
                <Box>
                  <Typography variant="subtitle2" fontWeight="bold">
                    {item.action}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    {item.description}
                  </Typography>
                </Box>
              </Box>
            </Grid>
          ))}
        </Grid>
      </Paper>
      
      {/* Badges and Achievements */}
      <Typography variant="h5" gutterBottom>
        Your Badges
      </Typography>
      
      <Grid container spacing={2} mb={4}>
        {rewards?.badges?.map((badge, index) => (
          <Grid item key={index}>
            <Tooltip title={`${badge.name}: ${badge.description}`} arrow>
              <Box
                sx={{
                  width: 80,
                  height: 80,
                  borderRadius: '50%',
                  bgcolor: 'primary.light',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  justifyContent: 'center',
                  p: 1,
                  textAlign: 'center',
                  boxShadow: 1,
                  position: 'relative',
                  overflow: 'hidden',
                }}
              >
                <Typography variant="h4" sx={{ lineHeight: 1 }}>
                  {badge.icon || '🏆'}
                </Typography>
                <Typography variant="caption" noWrap sx={{ width: '100%', fontSize: '0.6rem' }}>
                  {badge.name}
                </Typography>
                
                {badge.rare && (
                  <Box
                    sx={{
                      position: 'absolute',
                      top: 0,
                      right: 0,
                      width: 0,
                      height: 0,
                      borderStyle: 'solid',
                      borderWidth: '0 30px 30px 0',
                      borderColor: 'transparent #ffeb3b transparent transparent',
                    }}
                  >
                    <Typography
                      variant="caption"
                      sx={{
                        position: 'absolute',
                        top: 2,
                        right: -25,
                        transform: 'rotate(45deg)',
                        fontSize: '0.6rem',
                        color: 'black',
                        fontWeight: 'bold',
                      }}
                    >
                      RARE
                    </Typography>
                  </Box>
                )}
              </Box>
            </Tooltip>
          </Grid>
        ))}
      </Grid>
      
      {/* Referral Program */}
      <Paper sx={{ p: 3, mb: 4, bgcolor: 'secondary.light' }}>
        <Grid container alignItems="center" spacing={3}>
          <Grid item xs={12} md={8}>
            <Typography variant="h6" gutterBottom>
              Invite Friends & Earn Points
            </Typography>
            <Typography variant="body1" paragraph>
              Share your referral link and earn 25 points for each friend who signs up and submits a report.
            </Typography>
            
            <Box display="flex" mt={2}>
              <Box flexGrow={1} mr={1}>
                <Paper
                  variant="outlined"
                  sx={{
                    p: '6px 16px',
                    borderRadius: 1,
                    bgcolor: 'background.paper',
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                    whiteSpace: 'nowrap',
                  }}
                >
                  {`https://billboardcompliance.com/ref/${rewards?.referral_code || 'yourcode'}`}
                </Paper>
              </Box>
              <Button 
                variant="contained" 
                color="primary"
                onClick={() => {
                  navigator.clipboard.writeText(`https://billboardcompliance.com/ref/${rewards?.referral_code || 'yourcode'}`);
                  // Show success message
                }}
              >
                Copy
              </Button>
            </Box>
            
            <Typography variant="caption" display="block" mt={1}>
              {rewards?.referral_count || 0} friends joined • {rewards?.referral_points || 0} points earned
            </Typography>
          </Grid>
          <Grid item xs={12} md={4} textAlign="center">
            <Box
              sx={{
                width: 120,
                height: 120,
                borderRadius: '50%',
                bgcolor: 'primary.main',
                color: 'primary.contrastText',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                justifyContent: 'center',
                mx: 'auto',
                boxShadow: 3,
              }}
            >
              <Typography variant="h4">25</Typography>
              <Typography variant="subtitle2">POINTS</Typography>
              <Typography variant="caption" display="block">per referral</Typography>
            </Box>
          </Grid>
        </Grid>
      </Paper>
    </Box>
  );
};

export default Rewards;
