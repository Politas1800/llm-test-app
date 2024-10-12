import React, { useState } from 'react';
import { Box, Button, FormControl, FormLabel, Input, VStack, useToast } from '@chakra-ui/react';
import axios from 'axios';
import { API_BASE_URL } from '../config';

const Register = () => {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const toast = useToast();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post(`${API_BASE_URL}/register`, {
        username,
        email,
        hashed_password: password,
      });
      toast({
        title: 'Registration successful',
        description: "You've successfully registered as a Viewer.",
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
      // Redirect to login page or handle successful registration
    } catch (error) {
      toast({
        title: 'Registration failed',
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
            <FormLabel>Email</FormLabel>
            <Input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
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
            Register
          </Button>
        </VStack>
      </form>
    </Box>
  );
};

export default Register;
