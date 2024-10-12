import React, { useState, useEffect } from 'react';
import { Box, Heading, Text, VStack, Button, useToast, Table, Thead, Tbody, Tr, Th, Td } from '@chakra-ui/react';
import { CheckCircleIcon, WarningIcon } from '@chakra-ui/icons';
import { useParams } from 'react-router-dom';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const TestViewPage = () => {
  const { testId } = useParams();
  const [test, setTest] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const toast = useToast();

  useEffect(() => {
    const fetchTestData = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/tests/${testId}`);
        setTest(response.data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching test data:', error);
        setError(error.response?.data?.detail || 'An unexpected error occurred');
        setLoading(false);
        toast({
          title: 'Error fetching test data',
          description: error.response?.data?.detail || 'An unexpected error occurred',
          status: 'error',
          duration: 5000,
          isClosable: true,
        });
      }
    };

    fetchTestData();
  }, [testId, toast]);

  const handlePublish = async () => {
    try {
      await axios.post(`http://localhost:8000/tests/${testId}/publish`);
      setTest({ ...test, published: true });
      toast({
        title: 'Test published successfully',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
    } catch (error) {
      console.error('Error publishing test:', error);
      toast({
        title: 'Error publishing test',
        description: error.response?.data?.detail || 'An unexpected error occurred',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  if (loading) {
    return <Box>Loading...</Box>;
  }

  if (error) {
    return <Box>Error: {error}</Box>;
  }

  if (!test) {
    return <Box>Test not found</Box>;
  }

  const chartData = test.results?.map((result) => ({
    name: result.model,
    accuracy: (result.review_result === 'TRUE' ? 1 : 0) * 100,
  })) || [];

  const isAuthenticated = !!localStorage.getItem('token');

  return (
    <Box maxWidth="800px" margin="auto" mt={8}>
      <VStack spacing={8} align="stretch">
        <Heading>{test.title}</Heading>

        {/* Test Details */}
        <Box>
          <Heading size="md">Test Details</Heading>
          <Text>Description: {test.description}</Text>
          <Text>User Message: {test.user_message}</Text>
          <Text>Review Message: {test.review_message}</Text>
          <Text>Number of Requests: {test.num_requests}</Text>
          <Text>Published: {test.published ? 'Yes' : 'No'}</Text>
        </Box>

        {/* LLM Models Tested */}
        <Box>
          <Heading size="md">Anthropic Models Tested</Heading>
          <Table variant="simple">
            <Thead>
              <Tr>
                <Th>Model</Th>
                <Th>Result</Th>
                <Th>Response</Th>
              </Tr>
            </Thead>
            <Tbody>
              {test.results?.map((result, index) => (
                <Tr key={index}>
                  <Td>{result.model}</Td>
                  <Td>
                    {result.review_result === 'TRUE' ? (
                      <CheckCircleIcon color="green.500" />
                    ) : (
                      <WarningIcon color="red.500" />
                    )}
                  </Td>
                  <Td>{result.response}</Td>
                </Tr>
              ))}
            </Tbody>
          </Table>
        </Box>

        {/* Results Visualization */}
        <Box>
          <Heading size="md">Results</Heading>
          {chartData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="accuracy" fill="#8884d8" name="Accuracy (%)" />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <Text>No results available</Text>
          )}
        </Box>

        {/* Publish Button (only for authenticated users and unpublished tests) */}
        {isAuthenticated && !test.published && (
          <Button colorScheme="blue" onClick={handlePublish}>
            Publish Test Results
          </Button>
        )}
      </VStack>
    </Box>
  );
};

export default TestViewPage;
