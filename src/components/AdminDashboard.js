import React, { useState, useEffect } from 'react';
import { Box, Heading, Table, Thead, Tbody, Tr, Th, Td, Select, useToast, Button } from '@chakra-ui/react';
import axios from 'axios';
import { API_BASE_URL } from '../config';

const AdminDashboard = () => {
  const [users, setUsers] = useState([]);
  const toast = useToast();

  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/users`, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });
      setUsers(response.data);
    } catch (error) {
      toast({
        title: 'Error fetching users',
        description: error.response?.data?.detail || 'An error occurred',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    }
  };

  const handleRoleChange = async (userId, newRole) => {
    try {
      await axios.put(`${API_BASE_URL}/users/${userId}/role`,
        { new_role: newRole },
        { headers: { Authorization: `Bearer ${localStorage.getItem('token')}` } }
      );
      toast({
        title: 'Role updated',
        description: `User role updated to ${newRole}`,
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
      fetchUsers(); // Refresh the user list
    } catch (error) {
      toast({
        title: 'Error updating role',
        description: error.response?.data?.detail || 'An error occurred',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
    }
  };

  return (
    <Box maxWidth="800px" margin="auto" mt={8}>
      <Heading mb={4}>Admin Dashboard</Heading>
      <Table variant="simple">
        <Thead>
          <Tr>
            <Th>Username</Th>
            <Th>Email</Th>
            <Th>Current Role</Th>
            <Th>Change Role</Th>
            <Th>Action</Th>
          </Tr>
        </Thead>
        <Tbody>
          {users.map((user) => (
            <Tr key={user.id}>
              <Td>{user.username}</Td>
              <Td>{user.email}</Td>
              <Td>{user.role}</Td>
              <Td>
                <Select
                  value={user.role}
                  onChange={(e) => handleRoleChange(user.id, e.target.value)}
                >
                  <option value="Viewer">Viewer</option>
                  <option value="Creator">Creator</option>
                  <option value="Admin">Admin</option>
                </Select>
              </Td>
              <Td>
                <Button onClick={() => handleRoleChange(user.id, user.role)} colorScheme="blue">
                  Update Role
                </Button>
              </Td>
            </Tr>
          ))}
        </Tbody>
      </Table>
    </Box>
  );
};

export default AdminDashboard;
