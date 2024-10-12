import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Box, Heading, Text, VStack } from '@chakra-ui/react';
import axios from 'axios';

const TestView = () => {
  const [test, setTest] = useState(null);
  const { id } = useParams();

  useEffect(() => {
    const fetchTest = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/tests/${id}`);
        setTest(response.data);
      } catch (error) {
        console.error('Error fetching test:', error);
      }
    };
    fetchTest();
  }, [id]);

  if (!test) {
    return <Text>Loading...</Text>;
  }

  return (
    <Box maxWidth="800px" margin="auto" mt={8}>
      <VStack spacing={4} align="stretch">
        <Heading>{test.title}</Heading>
        <Text>{test.description}</Text>
        <Text>User Message: {test.user_message}</Text>
        <Text>Review Message: {test.review_message}</Text>
        <Text>Number of Requests: {test.num_requests}</Text>
        <Text>Created At: {new Date(test.created_at).toLocaleString()}</Text>
        <Text>Updated At: {new Date(test.updated_at).toLocaleString()}</Text>
      </VStack>
    </Box>
  );
};

export default TestView;
