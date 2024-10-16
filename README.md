# LLM Test App

## Project Overview

LLM Test App is a React application that allows users to create, run, and publish tests for Language Models (LLMs). The application uses Chakra UI for styling and Axios for API requests.

## Installation Instructions

To set up the project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/Politas1800/llm-test-app.git
   cd llm-test-app
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Run the development server:
   ```bash
   npm start
   ```

## Troubleshooting

If you encounter the error `npm error code ENOTEMPTY`, follow these steps:

### Clear the `node_modules` directory

1. Delete the `node_modules` directory manually or by running the command:
   ```bash
   rm -rf node_modules
   ```
2. Run the `npm install` command again:
   ```bash
   npm install
   ```

### Clear the npm cache

1. Clear the npm cache by running the following command:
   ```bash
   npm cache clean --force
   ```
2. Delete the `node_modules` directory manually or by running the command:
   ```bash
   rm -rf node_modules
   ```
3. Run the `npm install` command again:
   ```bash
   npm install
   ```

### Use a different package manager

If the issue persists, you can try using a different package manager like Yarn:

1. Install Yarn if you haven't already:
   ```bash
   npm install -g yarn
   ```
2. Delete the `node_modules` directory manually or by running the command:
   ```bash
   rm -rf node_modules
   ```
3. Install dependencies using Yarn:
   ```bash
   yarn install
   ```

## Available Scripts

In the project directory, you can run:

### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### `npm run eject`

**Note: this is a one-way operation. Once you `eject`, you can't go back!**

If you aren't satisfied with the build tool and configuration choices, you can `eject` at any time. This command will remove the single build dependency from your project.

Instead, it will copy all the configuration files and the transitive dependencies (webpack, Babel, ESLint, etc) right into your project so you have full control over them. All of the commands except `eject` will still work, but they will point to the copied scripts so you can tweak them. At this point you're on your own.

You don't have to ever use `eject`. The curated feature set is suitable for small and middle deployments, and you shouldn't feel obligated to use this feature. However we understand that this tool wouldn't be useful if you couldn't customize it when you are ready for it.

## Project Structure

The project structure is as follows:

- `public/`: Contains static files like `public/index.html` and `public/manifest.json`
- `src/`: Contains the main application code, including components, styles, and configuration files

## Configuration

The project uses the following configuration files and environment variables:

- `src/config.js`: Contains the backend API URL and other configuration variables

## Usage

To use the application, follow these steps:

1. Register a new user
2. Log in with the registered user
3. Navigate through the application:
   - Access the admin dashboard
   - Create tests
   - View tests

## API Endpoints

The application uses the following API endpoints:

- `POST /register`: Register a new user
- `POST /token`: Log in and obtain a token
- `GET /users/me`: Get the current user's information
- `GET /users`: Get a list of all users (admin only)
- `PUT /users/:userId/role`: Update a user's role (admin only)
- `POST /tests/create`: Create a new test
- `GET /tests`: Get a list of all tests
- `GET /tests/published`: Get a list of published tests
- `GET /tests/:testId`: Get a specific test by ID
- `POST /tests/:testId/publish`: Publish a test

## Contributing

To contribute to the project, follow these guidelines:

1. Submit issues and feature requests through the GitHub issue tracker
2. Create pull requests for bug fixes and new features
3. Follow the coding standards and guidelines

## License

This project is licensed under the MIT License.

## Acknowledgements

This project uses the following libraries and tools:

- [React](https://reactjs.org/)
- [Chakra UI](https://chakra-ui.com/)
- [Axios](https://axios-http.com/)
