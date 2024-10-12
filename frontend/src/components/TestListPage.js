import React, { useState, useEffect } from 'react';
import { Box, Heading, Table, Thead, Tbody, Tr, Th, Td, Button, useToast } from '@chakra-ui/react';
import axios from 'axios';
import { Link } from 'react-router-dom';
import { API_BASE_URL } from '../config';

const TestListPage = () => {
  const [tests, setTests] = useState([]);
  const [loading, setLoading] = useState(true);
  const toast = useToast();

  useEffect(() => {
    fetchTests();
  }, []);

  const fetchTests = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/tests`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });
      setTests(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching tests:', error);
      toast({
        title: 'Error fetching tests',
        description: error.response?.data?.detail || 'An unexpected error occurred',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
      setLoading(false);
    }
  };

  const handleDelete = async (testId) => {
    try {
      await axios.delete(`${API_BASE_URL}/tests/${testId}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`,
        },
      });
      toast({
        title: 'Test deleted',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
      fetchTests();
    } catch (error) {
      console.error('Error deleting test:', error);
      toast({
        title: 'Error deleting test',
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

  return (
    <Box maxWidth="1200px" margin="auto" mt={8}>
      <Heading mb={4}>Test List</Heading>
      <Table variant="simple">
        <Thead>
          <Tr>
            <Th>Title</Th>
            <Th>Description</Th>
            <Th>Created At</Th>
            <Th>Actions</Th>
          </Tr>
        </Thead>
        <Tbody>
          {tests.map((test) => (
            <Tr key={test.id}>
              <Td>{test.title}</Td>
              <Td>{test.description}</Td>
              <Td>{new Date(test.created_at).toLocaleString()}</Td>
              <Td>
                <Button as={Link} to={`/test/${test.id}`} colorScheme="blue" size="sm" mr={2}>
                  View
                </Button>
                <Button colorScheme="red" size="sm" onClick={() => handleDelete(test.id)}>
                  Delete
                </Button>
              </Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
    </Box>
  );
};

export default TestListPage;
