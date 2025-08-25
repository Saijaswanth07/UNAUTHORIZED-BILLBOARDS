import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  Table, 
  TableBody, 
  TableCell, 
  TableContainer, 
  TableHead, 
  TableRow, 
  Avatar, 
  TablePagination,
  Tabs,
  Tab,
  Divider,
  Badge,
  Tooltip
} from '@mui/material';
import { styled } from '@mui/material/styles';
import { publicApi } from '../../services/api';

const StyledTableRow = styled(TableRow)(({ theme }) => ({
  '&:nth-of-type(odd)': {
    backgroundColor: theme.palette.action.hover,
  },
  // hide last border
  '&:last-child td, &:last-child th': {
    border: 0,
  },
}));

const PodiumStep = styled(Box)(({ rank, theme }) => ({
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  padding: theme.spacing(2),
  backgroundColor: theme.palette.background.paper,
  borderRadius: theme.shape.borderRadius,
  boxShadow: theme.shadows[2],
  height: rank === 1 ? 200 : rank === 2 ? 160 : 120,
  justifyContent: 'flex-end',
  position: 'relative',
  '&::after': {
    content: '""',
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    height: 4,
    backgroundColor: 
      rank === 1 ? '#FFD700' : 
      rank === 2 ? '#C0C0C0' : 
      '#CD7F32',
  },
}));

const Leaderboard = () => {
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(0);
  const [rowsPerPage, setRowsPerPage] = useState(10);
  const [timeRange, setTimeRange] = useState('all');
  const [topUsers, setTopUsers] = useState([]);

  useEffect(() => {
    const fetchLeaderboard = async () => {
      try {
        setLoading(true);
        const data = await publicApi.fetchLeaderboard(100);
        setLeaderboard(data);
        
        // Get top 3 users for podium
        setTopUsers(data.slice(0, 3));
      } catch (error) {
        console.error('Error fetching leaderboard:', error);
      } finally {
        setLoading(false);
      }
    };
    
    fetchLeaderboard();
  }, [timeRange]);

  const handleChangePage = (event, newPage) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (event) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  const handleTabChange = (event, newValue) => {
    setTimeRange(newValue);
    setPage(0);
  };

  // Filter leaderboard based on time range
  const filteredLeaderboard = leaderboard.filter(user => {
    if (timeRange === 'all') return true;
    // Implement time-based filtering if needed
    return true;
  });

  // Get current user's rank (simulated)
  const currentUserRank = leaderboard.findIndex(user => user.user_id === 'current-user-id') + 1;
  const currentUser = leaderboard.find(user => user.user_id === 'current-user-id') || {
    username: 'You',
    score: 0,
    reports: 0,
    rank: currentUserRank || leaderboard.length + 1
  };

  return (
    <Box>
      <Typography variant="h5" gutterBottom>
        Leaderboard
      </Typography>
      
      <Tabs 
        value={timeRange} 
        onChange={handleTabChange} 
        aria-label="leaderboard time range"
        sx={{ mb: 3 }}
      >
        <Tab label="All Time" value="all" />
        <Tab label="This Month" value="month" />
        <Tab label="This Week" value="week" />
      </Tabs>
      
      {/* Podium */}
      <Box display="flex" justifyContent="center" mb={4} gap={3}>
        {topUsers[1] && (
          <PodiumStep rank={2}>
            <Typography variant="h6" color="textSecondary">2nd</Typography>
            <Avatar 
              alt={topUsers[1].username} 
              src={topUsers[1].avatar}
              sx={{ width: 60, height: 60, mb: 1 }}
            />
            <Typography variant="subtitle1" fontWeight="bold">
              {topUsers[1].username}
            </Typography>
            <Typography variant="body2" color="primary">
              {topUsers[1].score} pts
            </Typography>
          </PodiumStep>
        )}
        
        {topUsers[0] && (
          <PodiumStep rank={1} sx={{ transform: 'translateY(-20px)' }}>
            <Box display="flex" alignItems="center" mb={1}>
              <Typography variant="h5" color="textSecondary" mr={1}>👑</Typography>
              <Typography variant="h6">1st</Typography>
            </Box>
            <Badge
              overlap="circular"
              anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
              badgeContent={
                <Box sx={{ 
                  bgcolor: 'gold', 
                  color: 'black',
                  borderRadius: '50%',
                  width: 24,
                  height: 24,
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '0.75rem',
                  fontWeight: 'bold',
                }}>
                  #1
                </Box>
              }
            >
              <Avatar 
                alt={topUsers[0].username} 
                src={topUsers[0].avatar}
                sx={{ width: 80, height: 80, mb: 1, border: '3px solid gold' }}
              />
            </Badge>
            <Typography variant="h6" fontWeight="bold">
              {topUsers[0].username}
            </Typography>
            <Typography variant="body1" color="primary" fontWeight="bold">
              {topUsers[0].score} pts
            </Typography>
            <Typography variant="caption" color="textSecondary">
              {topUsers[0].reports} reports
            </Typography>
          </PodiumStep>
        )}
        
        {topUsers[2] && (
          <PodiumStep rank={3}>
            <Typography variant="h6" color="textSecondary">3rd</Typography>
            <Avatar 
              alt={topUsers[2].username} 
              src={topUsers[2].avatar}
              sx={{ width: 50, height: 50, mb: 1 }}
            />
            <Typography variant="subtitle1" fontWeight="bold">
              {topUsers[2].username}
            </Typography>
            <Typography variant="body2" color="primary">
              {topUsers[2].score} pts
            </Typography>
          </PodiumStep>
        )}
      </Box>
      
      {/* Current User Rank */}
      <Paper sx={{ p: 2, mb: 3, bgcolor: 'primary.light', color: 'primary.contrastText' }}>
        <Box display="flex" justifyContent="space-between" alignItems="center">
          <Box>
            <Typography variant="subtitle2">Your Rank</Typography>
            <Typography variant="h6">
              #{currentUser.rank} out of {leaderboard.length} users
            </Typography>
          </Box>
          <Box textAlign="right">
            <Typography variant="subtitle2">Your Score</Typography>
            <Typography variant="h6">{currentUser.score} points</Typography>
          </Box>
          <Box textAlign="right">
            <Typography variant="subtitle2">Your Reports</Typography>
            <Typography variant="h6">{currentUser.reports} reports</Typography>
          </Box>
        </Box>
      </Paper>
      
      {/* Leaderboard Table */}
      <Paper sx={{ width: '100%', overflow: 'hidden' }}>
        <TableContainer sx={{ maxHeight: 440 }}>
          <Table stickyHeader aria-label="leaderboard table">
            <TableHead>
              <TableRow>
                <TableCell>Rank</TableCell>
                <TableCell>User</TableCell>
                <TableCell align="right">Points</TableCell>
                <TableCell align="right">Reports</TableCell>
                <TableCell>Badges</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filteredLeaderboard
                .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
                .map((user, index) => (
                  <StyledTableRow 
                    key={user.user_id}
                    hover
                    selected={user.user_id === 'current-user-id'}
                  >
                    <TableCell component="th" scope="row">
                      <Box display="flex" alignItems="center">
                        {index + 1 + page * rowsPerPage === 1 && '🥇'}
                        {index + 1 + page * rowsPerPage === 2 && '🥈'}
                        {index + 1 + page * rowsPerPage === 3 && '🥉'}
                        {index + 1 + page * rowsPerPage > 3 && (
                          <Typography variant="body2" sx={{ ml: 1 }}>
                            #{index + 1 + page * rowsPerPage}
                          </Typography>
                        )}
                      </Box>
                    </TableCell>
                    <TableCell>
                      <Box display="flex" alignItems="center">
                        <Avatar 
                          alt={user.username} 
                          src={user.avatar}
                          sx={{ width: 32, height: 32, mr: 1 }}
                        />
                        <Typography variant="body2">
                          {user.username}
                          {user.is_current_user && ' (You)'}
                        </Typography>
                      </Box>
                    </TableCell>
                    <TableCell align="right">
                      <Tooltip title={`${user.score} points`}>
                        <Box>
                          <Box 
                            sx={{
                              height: 8,
                              bgcolor: 'primary.main',
                              borderRadius: 4,
                              width: `${Math.min(100, (user.score / (leaderboard[0]?.score || 1)) * 100)}%`,
                              float: 'right'
                            }}
                          />
                          {user.score}
                        </Box>
                      </Tooltip>
                    </TableCell>
                    <TableCell align="right">
                      {user.reports}
                    </TableCell>
                    <TableCell>
                      <Box display="flex" gap={1}>
                        {user.badges?.map((badge, i) => (
                          <Tooltip key={i} title={badge.name}>
                            <Box sx={{ 
                              bgcolor: 'primary.light', 
                              color: 'primary.contrastText',
                              borderRadius: '50%',
                              width: 24,
                              height: 24,
                              display: 'flex',
                              alignItems: 'center',
                              justifyContent: 'center',
                              fontSize: '0.75rem',
                            }}>
                              {badge.icon}
                            </Box>
                          </Tooltip>
                        ))}
                      </Box>
                    </TableCell>
                  </StyledTableRow>
                ))}
            </TableBody>
          </Table>
        </TableContainer>
        <TablePagination
          rowsPerPageOptions={[5, 10, 25]}
          component="div"
          count={filteredLeaderboard.length}
          rowsPerPage={rowsPerPage}
          page={page}
          onPageChange={handleChangePage}
          onRowsPerPageChange={handleChangeRowsPerPage}
        />
      </Paper>
      
      <Box mt={4}>
        <Typography variant="h6" gutterBottom>
          How to Earn Points
        </Typography>
        <Box display="grid" gridTemplateColumns="repeat(auto-fill, minmax(250px, 1fr))" gap={2}>
          <Paper sx={{ p: 2 }}>
            <Typography color="primary" variant="h6">Submit a Report</Typography>
            <Typography variant="body2">+10 points</Typography>
          </Paper>
          <Paper sx={{ p: 2 }}>
            <Typography color="primary" variant="h6">Report Verified</Typography>
            <Typography variant="body2">+20 points</Typography>
          </Paper>
          <Paper sx={{ p: 2 }}>
            <Typography color="primary" variant="h6">Daily Streak</Typography>
            <Typography variant="body2">+5 points per day</Typography>
          </Paper>
          <Paper sx={{ p: 2 }}>
            <Typography color="primary" variant="h6">Refer a Friend</Typography>
            <Typography variant="body2">+25 points</Typography>
          </Paper>
        </Box>
      </Box>
    </Box>
  );
};

export default Leaderboard;
