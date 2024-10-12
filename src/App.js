import React, { useState, useEffect } from 'react';
import { ChakraProvider, Box, VStack, Heading, Button } from '@chakra-ui/react';
import { BrowserRouter as Router, Route, Routes, Link, Navigate } from 'react-router-dom';
import Register from './components/Register';
import Login from './components/Login';
import AdminDashboard from './components/AdminDashboard';
import HomePage from './components/HomePage';
import TestViewPage from './components/TestViewPage';
import TestListPage from './components/TestListPage';
import CreateTestPage from './components/CreateTestPage';
import { API_BASE_URL } from './config';

function App() {
  const [userRole, setUserRole] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);

  useEffect(() => {
    const fetchUserRole = async () => {
      const token = localStorage.getItem('token');
      if (token) {
        try {
          const response = await fetch(`${API_BASE_URL}/users/me`, {
            headers: { Authorization: `Bearer ${token}` }
          });
          if (response.ok) {
            const userData = await response.json();
            setUserRole(userData.role);
            setIsAuthenticated(true);
          } else {
            // If the token is invalid, clear it
            localStorage.removeItem('token');
            setIsAuthenticated(false);
            setUserRole(null);
          }
        } catch (error) {
          console.error('Error fetching user role:', error);
          setIsAuthenticated(false);
          setUserRole(null);
        }
      } else {
        setIsAuthenticated(false);
        setUserRole(null);
      }
    };
    fetchUserRole();
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
    setUserRole(null);
  };

  return (
    <ChakraProvider>
      <Router>
        <Box>
          <VStack spacing={8} align="center" py={8}>
            <Heading>LLM Test App</Heading>
            <nav>
              <Link to="/" style={{ marginRight: '10px' }}>Home</Link>
              {!isAuthenticated && (
                <>
                  <Link to="/register" style={{ marginRight: '10px' }}>Register</Link>
                  <Link to="/login" style={{ marginRight: '10px' }}>Login</Link>
                </>
              )}
              {isAuthenticated && (
                <>
                  {(userRole === 'Admin' || userRole === 'Creator') && (
                    <>
                      <Link to="/admin" style={{ marginRight: '10px' }}>Admin Dashboard</Link>
                      <Link to="/tests" style={{ marginRight: '10px' }}>Test List</Link>
                      <Link to="/create-test" style={{ marginRight: '10px' }}>Create Test</Link>
                    </>
                  )}
                  <Button onClick={handleLogout}>Logout</Button>
                </>
              )}
            </nav>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/register" element={<Register />} />
              <Route path="/login" element={<Login setIsAuthenticated={setIsAuthenticated} setUserRole={setUserRole} />} />
              <Route
                path="/admin"
                element={
                  (userRole === 'Admin' || userRole === 'Creator') ? (
                    <AdminDashboard />
                  ) : (
                    <Navigate to="/" replace />
                  )
                }
              />
              <Route
                path="/tests"
                element={
                  (userRole === 'Admin' || userRole === 'Creator') ? (
                    <TestListPage />
                  ) : (
                    <Navigate to="/" replace />
                  )
                }
              />
              <Route
                path="/create-test"
                element={
                  (userRole === 'Admin' || userRole === 'Creator') ? (
                    <CreateTestPage />
                  ) : (
                    <Navigate to="/" replace />
                  )
                }
              />
              <Route path="/test/:testId" element={<TestViewPage />} />
            </Routes>
          </VStack>
        </Box>
      </Router>
    </ChakraProvider>
  );
}

export default App;
