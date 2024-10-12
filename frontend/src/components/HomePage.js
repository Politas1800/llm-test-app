import React, { useState, useEffect } from 'react';
import { Box, Heading, Text, VStack, Button, SimpleGrid } from '@chakra-ui/react';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { API_BASE_URL } from '../config';

const HomePage = () => {
  const [publishedTests, setPublishedTests] = useState([]);

  useEffect(() => {
    fetchPublishedTests();
  }, []);

  const fetchPublishedTests = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/tests/published`);
      setPublishedTests(response.data);
    } catch (error) {
      console.error('Error fetching published tests:', error);
    }
  };

  return (
    <Box maxWidth="800px" margin="auto" mt={8}>
      <VStack spacing={8} align="stretch">
        <Heading>Welcome to LLM Test App</Heading>
        <Text>
          This application allows you to create, run, and publish tests for Language Models (LLMs).
          Explore published tests below or log in to create your own!
        </Text>
        <Heading size="md">Published Tests</Heading>
        {publishedTests.length > 0 ? (
          <SimpleGrid columns={2} spacing={4}>
            {publishedTests.map((test) => (
              <Box key={test.id} p={4} borderWidth={1} borderRadius="md">
                <Heading size="sm">{test.title}</Heading>
                <Text mt={2} noOfLines={2}>{test.description}</Text>
                <Button as={Link} to={`/test/${test.id}`} mt={2} colorScheme="blue">
                  View Test
                </Button>
              </Box>
            ))}
          </SimpleGrid>
        ) : (
          <Text>No published tests available at the moment.</Text>
        )}
      </VStack>
    </Box>
  );
};

export default HomePage;
