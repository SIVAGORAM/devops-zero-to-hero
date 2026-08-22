# Amazon Cognito (Authentication) Interview Questions

Managing user sign-ups and passwords securely is difficult. These questions test your knowledge of Identity Providers, JWT tokens, and Web Identity Federation.

### 1. What is Amazon Cognito?
**Answer:** Amazon Cognito provides authentication, authorization, and user management for web and mobile apps. It allows you to easily add user sign-up and sign-in features and seamlessly supports federation with identity providers like Google, Facebook, Apple, and enterprise SAML integrations.

### 2. What is a Cognito User Pool?
**Answer:** A User Pool is a fully managed user directory. It handles user registration, authentication (passwords), account recovery, and Multi-Factor Authentication (MFA). When a user successfully logs in to a User Pool, Cognito returns a standard JSON Web Token (JWT) to the application.

### 3. What is a Cognito Identity Pool (Federated Identities)?
**Answer:** While User Pools give access to your *Application*, Identity Pools give users direct access to *AWS Resources*. An Identity Pool takes a token (from a User Pool, Google, or Facebook) and exchanges it for temporary, limited-privilege AWS IAM credentials (via STS) so the user's mobile app can upload a photo directly to S3.

### 4. What is Web Identity Federation?
**Answer:** It is the process of allowing users to authenticate using a well-known third-party Identity Provider (IdP) like Google or Facebook. Instead of creating a new username and password in your database, they log in with Google, and your application uses that token to grant them access. Cognito simplifies this entire flow.

### 5. How do User Pools and Identity Pools work together?
**Answer:** 
1. The user logs into the **User Pool** (using a password or SSO).
2. The User Pool issues an OIDC token (JWT).
3. The application passes that token to the **Identity Pool**.
4. The Identity Pool verifies the token and issues temporary AWS IAM credentials.
5. The application uses those credentials to securely write data to a DynamoDB table.

### 6. How can you customize the sign-up workflow in Cognito?
**Answer:** Cognito provides several AWS Lambda Triggers. You can write custom Lambda functions that execute at specific lifecycle events, such as `PreSignUp` (to auto-confirm users from a specific corporate domain) or `PostConfirmation` (to insert the new user's ID into your RDS database).

### 7. What is the Cognito Hosted UI?
**Answer:** Building secure login, sign-up, and password-reset pages from scratch is time-consuming and risky. The Hosted UI is an OAuth 2.0 compliant, customizable, out-of-the-box web page hosted by AWS that handles the entire authentication flow securely for your application.

### 8. How do you secure an API Gateway endpoint using Cognito?
**Answer:** You configure a **Cognito User Pool Authorizer** directly on the API Gateway method. When the client makes an HTTP request, they must include their JWT token in the `Authorization` header. API Gateway automatically validates the token's signature against Cognito before allowing the request to reach your Lambda function.

### 9. Does Cognito support Multi-Factor Authentication (MFA)?
**Answer:** Yes. Cognito User Pools natively support SMS text messages and Time-based One-Time Passwords (TOTP) using authenticator apps (like Google Authenticator) to provide a second layer of security during sign-in.

### 10. What is Cognito Sync?
**Answer:** Cognito Sync is a legacy service used to synchronize user profile data (like app preferences or game state) across multiple mobile devices. AWS now strongly recommends using AWS AppSync (GraphQL) for this functionality instead.
