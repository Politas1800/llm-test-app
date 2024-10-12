import React, { useState } from 'react';
import { Box, Button, FormControl, FormLabel, Input, VStack, useToast } from '@chakra-ui/react';
import axios from 'axios';
import { API_BASE_URL } from '../config';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const toast = useToast();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${API_BASE_URL}/token`, {
        username,
        password,
      }, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      });

      localStorage.setItem('token', response.data.access_token);
      toast({
        title: 'Login successful',
        description: "You've successfully logged in.",
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
      navigate('/'); // Redirect to home page after successful login
    } catch (error) {
      toast({
        title: 'Login failed',
        description: error.response?.data?.detail || 'An error occurred',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    }
  };

  return (
    <Box maxWidth="400px" margin="auto" mt={8}>
      <form onSubmit={handleSubmit}>
        <VStack spacing={4}>
          <FormControl isRequired>
            <FormLabel>Username</FormLabel>
            <Input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
            />
          </FormControl>
          <FormControl isRequired>
            <FormLabel>Password</FormLabel>
            <Input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </FormControl>
          <Button type="submit" colorScheme="blue">
            Login
          </Button>
        </VStack>
      </form>
    </Box>
  );
};

export default Login;
