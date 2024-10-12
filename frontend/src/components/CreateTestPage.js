import React, { useState } from 'react';
import axios from 'axios';
import { API_BASE_URL } from '../config';
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  VStack,
  Heading,
  Textarea,
  NumberInput,
  NumberInputField,
  NumberInputStepper,
  NumberIncrementStepper,
  NumberDecrementStepper,
  Select,
  Flex,
  useToast,
} from '@chakra-ui/react';

const CreateTestPage = () => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [userMessage, setUserMessage] = useState('');
  const [reviewMessage, setReviewMessage] = useState('');
  const [numRequests, setNumRequests] = useState(1);
  const [selectedLLMs, setSelectedLLMs] = useState([{ model: '' }]);
  const [isLoading, setIsLoading] = useState(false);
  const toast = useToast();

  const llmProviders = {
    Anthropic: ['claude-3-opus-20240229', 'claude-3-haiku-20240307', 'claude-3-5-sonnet-20240620'],
  };

  const handleAddLLM = () => {
    setSelectedLLMs([...selectedLLMs, { model: '' }]);
  };

  const handleLLMChange = (index, value) => {
    const updatedLLMs = [...selectedLLMs];
    updatedLLMs[index].model = value;
    setSelectedLLMs(updatedLLMs);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const response = await axios.post(`${API_BASE_URL}/tests/create`, {
        title,
        description,
        user_message: userMessage,
        review_message: reviewMessage,
        num_requests: numRequests,
        selected_llms: selectedLLMs.map(llm => llm.model),
      });

      toast({
        title: 'Test created successfully',
        description: `Test ID: ${response.data.id}`,
        status: 'success',
        duration: 5000,
        isClosable: true,
      });

      // Reset form
      setTitle('');
      setDescription('');
      setUserMessage('');
      setReviewMessage('');
      setNumRequests(1);
      setSelectedLLMs([{ model: '' }]);
    } catch (error) {
      toast({
        title: 'Error creating test',
        description: error.response?.data?.detail || 'An unexpected error occurred',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Box maxWidth="800px" margin="auto" mt={8}>
      <Heading mb={4}>Create New Test</Heading>
      <form onSubmit={handleSubmit}>
        <VStack spacing={4} align="stretch">
          <FormControl isRequired>
            <FormLabel>Title</FormLabel>
            <Input
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Enter test title"
            />
          </FormControl>
          <FormControl isRequired>
            <FormLabel>Description</FormLabel>
            <Textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Enter test description"
            />
          </FormControl>
          <FormControl isRequired>
            <FormLabel>User Message</FormLabel>
            <Textarea
              value={userMessage}
              onChange={(e) => setUserMessage(e.target.value)}
              placeholder="Enter the user message for the test"
            />
          </FormControl>
          <FormControl isRequired>
            <FormLabel>Review Message</FormLabel>
            <Textarea
              value={reviewMessage}
              onChange={(e) => setReviewMessage(e.target.value)}
              placeholder="Enter the review message for the test"
            />
          </FormControl>
          <FormControl isRequired>
            <FormLabel>Number of Requests</FormLabel>
            <NumberInput min={1} value={numRequests} onChange={(value) => setNumRequests(parseInt(value))}>
              <NumberInputField />
              <NumberInputStepper>
                <NumberIncrementStepper />
                <NumberDecrementStepper />
              </NumberInputStepper>
            </NumberInput>
          </FormControl>
          {selectedLLMs.map((llm, index) => (
            <FormControl key={index} isRequired>
              <FormLabel>Anthropic Model</FormLabel>
              <Select
                value={llm.model}
                onChange={(e) => handleLLMChange(index, e.target.value)}
              >
                <option value="">Select Model</option>
                {llmProviders.Anthropic.map((model) => (
                  <option key={model} value={model}>
                    {model}
                  </option>
                ))}
              </Select>
            </FormControl>
          ))}
          <Button onClick={handleAddLLM}>Add Another Model</Button>
          <Button type="submit" colorScheme="blue" isLoading={isLoading}>
            Run Test
          </Button>
        </VStack>
      </form>
    </Box>
  );
};

export default CreateTestPage;
