import React, { useState, useEffect, useRef } from 'react';
import mapboxgl from 'mapbox-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import { Box, Typography, Paper, Select, MenuItem, FormControl, InputLabel } from '@mui/material';
import { styled } from '@mui/material/styles';
import { fetchHeatmapData } from '../../services/api';

// Initialize Mapbox token
mapboxgl.accessToken = process.env.REACT_APP_MAPBOX_TOKEN;

const MapContainer = styled(Box)(({ theme }) => ({
  width: '100%',
  height: '600px',
  borderRadius: theme.shape.borderRadius,
  overflow: 'hidden',
  boxShadow: theme.shadows[3],
}));

const DashboardContainer = styled(Box)({
  padding: '24px',
  maxWidth: '1400px',
  margin: '0 auto',
});

const StatsContainer = styled(Paper)(({ theme }) => ({
  padding: theme.spacing(3),
  marginBottom: theme.spacing(3),
  display: 'grid',
  gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
  gap: theme.spacing(2),
}));

const StatItem = styled(Box)(({ theme }) => ({
  textAlign: 'center',
  padding: theme.spacing(2),
  backgroundColor: theme.palette.grey[100],
  borderRadius: theme.shape.borderRadius,
}));

const HeatmapDashboard = () => {
  const [heatmapData, setHeatmapData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState(30);
  const [violationType, setViolationType] = useState('all');
  const [stats, setStats] = useState({
    totalViolations: 0,
    violationsByType: {},
    recentActivity: [],
  });
  
  const mapContainer = useRef(null);
  const map = useRef(null);
  const heatmapLayer = useRef(null);

  // Load heatmap data
  useEffect(() => {
    const loadData = async () => {
      try {
        setLoading(true);
        const data = await fetchHeatmapData({
          days: timeRange,
          violationType: violationType === 'all' ? null : violationType
        });
        setHeatmapData(data);
        
        // Update heatmap layer if map is already initialized
        if (map.current && heatmapLayer.current) {
          updateHeatmapLayer(data);
        }
      } catch (error) {
        console.error('Error loading heatmap data:', error);
      } finally {
        setLoading(false);
      }
    };
    
    loadData();
  }, [timeRange, violationType]);
  
  // Initialize map and heatmap
  useEffect(() => {
    if (!mapContainer.current) return;
    
    // Initialize map
    map.current = new mapboxgl.Map({
      container: mapContainer.current,
      style: 'mapbox://styles/mapbox/dark-v10', // Dark theme for better visualization
      center: [77.5946, 12.9716], // Default to Bangalore
      zoom: 11,
      pitch: 45,
      bearing: -17.6,
      antialias: true,
    });
    
    // Add navigation control
    map.current.addControl(new mapboxgl.NavigationControl());
    
    // Add geolocate control
    map.current.addControl(
      new mapboxgl.GeolocateControl({
        positionOptions: {
          enableHighAccuracy: true,
        },
        trackUserLocation: true,
      })
    );
    
    // Add scale control
    map.current.addControl(new mapboxgl.ScaleControl());
    
    // When map is loaded, add heatmap layer
    map.current.on('load', () => {
      updateHeatmapLayer(heatmapData);
    });
    
    return () => {
      if (map.current) {
        map.current.remove();
      }
    };
  }, []);
  
  // Update heatmap layer with new data
  const updateHeatmapLayer = (data) => {
    if (!map.current) return;
    
    // Remove existing heatmap layer if it exists
    if (map.current.getLayer('heatmap-layer')) {
      map.current.removeLayer('heatmap-layer');
      map.current.removeSource('heatmap');
    }
    
    if (data.length === 0) return;
    
    // Add heatmap source
    map.current.addSource('heatmap', {
      type: 'geojson',
      data: {
        type: 'FeatureCollection',
        features: data.map(point => ({
          type: 'Feature',
          geometry: {
            type: 'Point',
            coordinates: [point.longitude, point.latitude],
          },
          properties: {
            weight: point.weight,
            violation_type: point.violation_type,
            severity: point.severity,
            date: point.date,
          },
        })),
      },
    });
    
    // Add heatmap layer
    map.current.addLayer(
      {
        id: 'heatmap-layer',
        type: 'heatmap',
        source: 'heatmap',
        maxzoom: 15,
        paint: {
          // Increase heatmap weight based on frequency and property magnitude
          'heatmap-weight': [
            'interpolate',
            ['linear'],
            ['get', 'weight'],
            0, 0,
            6, 1,
          ],
          // Increase heatmap color weight by zoom level
          // heatmap-intensity is a multiplier on top of heatmap-weight
          'heatmap-intensity': [
            'interpolate',
            ['linear'],
            ['zoom'],
            0, 1,
            9, 3,
          ],
          // Color ramp for heatmap
          'heatmap-color': [
            'interpolate',
            ['linear'],
            ['heatmap-density'],
            0, 'rgba(33,102,172,0)',
            0.2, 'rgb(103,169,207)',
            0.4, 'rgb(209,229,240)',
            0.6, 'rgb(253,219,199)',
            0.8, 'rgb(239,138,98)',
            1, 'rgb(178,24,43)',
          ],
          // Adjust the heatmap radius by zoom level
          'heatmap-radius': [
            'interpolate',
            ['linear'],
            ['zoom'],
            0, 2,
            9, 20,
          ],
          // Transition from heatmap to circle layer by zoom level
          'heatmap-opacity': [
            'interpolate',
            ['linear'],
            ['zoom'],
            7, 1,
            9, 0,
          ],
        },
      },
      'waterway-label' // Insert before waterway labels
    );
    
    // Add a circle layer to show individual points at higher zoom levels
    map.current.addLayer(
      {
        id: 'points-layer',
        type: 'circle',
        source: 'heatmap',
        minzoom: 9,
        paint: {
          'circle-radius': [
            'interpolate',
            ['linear'],
            ['zoom'],
            7, [
              'interpolate',
              ['linear'],
              ['get', 'weight'],
              1, 4,
              6, 10,
            ],
            16, [
              'interpolate',
              ['linear'],
              ['get', 'weight'],
              1, 6,
              6, 30,
            ],
          ],
          'circle-color': [
            'match',
            ['get', 'severity'],
            'high', '#d73027',
            'medium', '#fdae61',
            'low', '#fee08b',
            /* other */ '#91cf60',
          ],
          'circle-stroke-width': 1,
          'circle-stroke-color': 'white',
          'circle-opacity': [
            'interpolate',
            ['linear'],
            ['zoom'],
            7, 0,
            8, 1,
          ],
        },
      },
      'waterway-label' // Insert before waterway labels
    );
    
    // Add click event to show popup
    map.current.on('click', 'points-layer', (e) => {
      if (e.features.length === 0) return;
      
      const feature = e.features[0];
      const coordinates = feature.geometry.coordinates.slice();
      const { violation_type, severity, date } = feature.properties;
      
      // Ensure that if the map is zoomed out such that multiple
      // copies of the feature are visible, the popup appears
      // over the copy being pointed to.
      while (Math.abs(e.lngLat.lng - coordinates[0]) > 180) {
        coordinates[0] += e.lngLat.lng > coordinates[0] ? 360 : -360;
      }
      
      new mapboxgl.Popup()
        .setLngLat(coordinates)
        .setHTML(
          `<strong>Violation Type:</strong> ${violation_type}<br>` +
          `<strong>Severity:</strong> ${severity}<br>` +
          `<strong>Date:</strong> ${new Date(date).toLocaleDateString()}`
        )
        .addTo(map.current);
    });
    
    // Change the cursor to a pointer when the mouse is over the points layer.
    map.current.on('mouseenter', 'points-layer', () => {
      if (map.current) map.current.getCanvas().style.cursor = 'pointer';
    });
    
    // Change it back to a pointer when it leaves.
    map.current.on('mouseleave', 'points-layer', () => {
      if (map.current) map.current.getCanvas().style.cursor = '';
    });
  };
  
  // Load stats
  useEffect(() => {
    const loadStats = async () => {
      try {
        const response = await fetch('/api/public/stats');
        const data = await response.json();
        setStats({
          totalViolations: data.total_violations,
          violationsByType: data.violations_by_type,
          recentActivity: data.recent_activity,
        });
      } catch (error) {
        console.error('Error loading stats:', error);
      }
    };
    
    loadStats();
  }, []);
  
  return (
    <DashboardContainer>
      <Typography variant="h4" component="h1" gutterBottom>
        Billboard Compliance Heatmap
      </Typography>
      
      <Paper sx={{ p: 3, mb: 3 }}>
        <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
          <Typography variant="h6">Violation Heatmap</Typography>
          
          <Box display="flex" gap={2}>
            <FormControl size="small" sx={{ minWidth: 200 }}>
              <InputLabel>Time Range</InputLabel>
              <Select
                value={timeRange}
                label="Time Range"
                onChange={(e) => setTimeRange(e.target.value)}
              >
                <MenuItem value={7}>Last 7 days</MenuItem>
                <MenuItem value={30}>Last 30 days</MenuItem>
                <MenuItem value={90}>Last 90 days</MenuItem>
                <MenuItem value={365}>Last year</MenuItem>
              </Select>
            </FormControl>
            
            <FormControl size="small" sx={{ minWidth: 200 }}>
              <InputLabel>Violation Type</InputLabel>
              <Select
                value={violationType}
                label="Violation Type"
                onChange={(e) => setViolationType(e.target.value)}
              >
                <MenuItem value="all">All Types</MenuItem>
                <MenuItem value="size">Size Violation</MenuItem>
                <MenuItem value="location">Location Violation</MenuItem>
                <MenuItem value="permit">Permit Violation</MenuItem>
                <MenuItem value="safety">Safety Violation</MenuItem>
              </Select>
            </FormControl>
          </Box>
        </Box>
        
        <MapContainer ref={mapContainer}>
          {loading && (
            <Box
              position="absolute"
              top={0}
              left={0}
              right={0}
              bottom={0}
              display="flex"
              alignItems="center"
              justifyContent="center"
              bgcolor="rgba(255, 255, 255, 0.7)"
              zIndex={1}
            >
              <Typography>Loading heatmap data...</Typography>
            </Box>
          )}
        </MapContainer>
      </Paper>
      
      <Typography variant="h5" gutterBottom>
        Statistics
      </Typography>
      
      <StatsContainer elevation={3}>
        <StatItem>
          <Typography variant="h4" color="primary">
            {stats.totalViolations.toLocaleString()}
          </Typography>
          <Typography variant="subtitle2">Total Violations</Typography>
        </StatItem>
        
        {Object.entries(stats.violationsByType).map(([type, count]) => (
          <StatItem key={type}>
            <Typography variant="h5">{count}</Typography>
            <Typography variant="subtitle2">
              {type.charAt(0).toUpperCase() + type.slice(1).replace('_', ' ')} Violations
            </Typography>
          </StatItem>
        ))}
      </StatsContainer>
      
      <Box mt={3}>
        <Typography variant="h5" gutterBottom>
          Recent Activity
        </Typography>
        
        <Paper>
          {stats.recentActivity.length > 0 ? (
            <ul style={{ padding: 0 }}>
              {stats.recentActivity.map((activity, index) => (
                <Box
                  key={index}
                  component="li"
                  p={2}
                  borderBottom={index < stats.recentActivity.length - 1 ? 1 : 0}
                  borderColor="divider"
                  display="flex"
                  justifyContent="space-between"
                >
                  <Box>
                    <Typography>
                      <strong>{activity.type}</strong> reported at {new Date(activity.timestamp).toLocaleString()}
                    </Typography>
                    <Typography variant="body2" color="textSecondary">
                      {activity.description}
                    </Typography>
                  </Box>
                  <Typography variant="caption" color="textSecondary">
                    {activity.location ? 
                      `${activity.location.lat.toFixed(4)}, ${activity.location.lng.toFixed(4)}` : 
                      'No location'}
                  </Typography>
                </Box>
              ))}
            </ul>
          ) : (
            <Box p={3} textAlign="center">
              <Typography color="textSecondary">
                No recent activity to display
              </Typography>
            </Box>
          )}
        </Paper>
      </Box>
    </DashboardContainer>
  );
};

export default HeatmapDashboard;
