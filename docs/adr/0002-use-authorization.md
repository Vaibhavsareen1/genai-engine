# Use JWT Authorization

### Table of Content
- [Use JWT Authorization](#use-jwt-authorization)
    - [Table of Content](#table-of-content)
  - [1. Problem Statement](#1-problem-statement)
  - [2. Stateful vs Stateless Architecture](#2-stateful-vs-stateless-architecture)
    - [2.1 Stateful Model](#21-stateful-model)
    - [2.2 Stateless Model](#22-stateless-model)
  - [3. Authentication vs Authorization](#3-authentication-vs-authorization)
    - [3.1 Authentication](#31-authentication)
    - [3.2 Authorization](#32-authorization)
  - [4. Types of Authorization](#4-types-of-authorization)
    - [4.1 Role Based Access Control (RBAC)](#41-role-based-access-control-rbac)
    - [4.2 Attribute Based Access Control (ABAC)](#42-attribute-based-access-control-abac)
    - [4.3 Relation Based Access Control (ReBAC)](#43-relation-based-access-control-rebac)
  - [5. Permission Packaging Processes](#5-permission-packaging-processes)
    - [5.1 Session based Authorization](#51-session-based-authorization)
    - [5.2 Third Party based Authorization (OAuth)](#52-third-party-based-authorization-oauth)
    - [5.3 JWT based Authorization](#53-jwt-based-authorization)
  - [6. Understanding JWT Authorization](#6-understanding-jwt-authorization)
    - [6.1 What is JWT](#61-what-is-jwt)
    - [6.2 The structure of JWT](#62-the-structure-of-jwt)
    - [6.3 Flow of JWT creation](#63-flow-of-jwt-creation)
    - [6.4 Flow of JWT verification](#64-flow-of-jwt-verification)
    - [6.5 JWT on Steroids](#65-jwt-on-steroids)
      - [6.5.1 JWE Token Creation Process](#651-jwe-token-creation-process)
      - [6.5.2 JWE Token Verification Process](#652-jwe-token-verification-process)
    - [6.6 Why JWT over JWE](#66-why-jwt-over-jwe)
  - [7 Conclusion](#7-conclusion)

## 1. Problem Statement
In the current world **data intensive applications** use AI/ML systems as services. The AI/ML services are internal components of the applications. The services are not directly exposed to the end users but are rather consumed by an **orchestration layer** that interacts with the end users.

These services still need to be secured even if they are sitting behind the orchestration layer. The challenge becomes how to add this security layer to the services

There are 2 broad modes of protection:
1. **Authentication**: The process of verifying the **identity** of a user, service or a device.
2. **Authorization**: It is the process of verifying if a user, service or device has the right **permissions** to use the service

This document is created for the following reasons:
1. **Technical Justification**: Document why **JWT Token based authorization** as a mode of protection should be used to protect the services and keep a record of architectural decision made for the choice of protection for the generative AI services.
2. **Educational purpose**: Serve as a reference for developers to leverage and understand the use of JWT based authorization building python based web applications.

## 2. Stateful vs Stateless Architecture
The choice of security mechanism is dictated by the architectural nature of the services There are broadly two types of architecture models:
1. **Stateful Model**
2. **Stateless Model**

### 2.1 Stateful Model
- Stateful model maintains a memory of previous actions to satisfy the current and future actions.
- The memory can be associated with a **"session id"**
- The server needs to store this "session id" and the client needs to provide this "session id" in order to unlock the memory associated with it to the server to provide a response for the current actions based on the previous states.
- To maintain the system of storing memory and the states there needs to be a centralised session stores which makes it difficult to scale such services
- An example of this type of service is feeds on social media platforms. Where without storing information from the previous actions. The platform would not be able to provide recommendations for what should be part of the feed that suits the taste of the user.

### 2.2 Stateless Model
- Stateless model treates every request as a "**clean slate**" where all of the information has to be provided as part of the current action.
- These services do not need to care about state management.
- Since the stateless model does not need to care about state management they dont need to maintain a centralised session store. This allows the services to be horizontally scalable as any server can handle the request making them ideal for **high throughput** workloads.
- An example of this type of model is summarization service. Where information about what needs to be summarized along with any other attributes that can affect the outcome such as the style, length of summarization, audience type etc needs to be provided and the service works on the information provided the summarized content as the end result back to the user.

In data intensive applications the AI/ML service components should remain **stateless**. The state management should be delegated to the **orchestrational layer**. 

Even **stateless services** need to be protected. Before the protocol for projection is decided it is important to understand the modes of protection which are authentication and authorization.

## 3. Authentication vs Authorization
To maintain a scalable stateless architecture we have to decouple identity verification from permission enforcement. 

### 3.1 Authentication
- It is the process of verifying the identity of a user, service or device.
- It is the process to check if the user, service or device are the one whom they claim to be.
- For proper identification information of the user, service or device needs to persist at the time of their registration with the application.
- **State management** needs to be done in order to perform the same process of identification in the future

### 3.2 Authorization
- It is the process of verifying if a user, service or device has the right permissions to use the service
- The permissions are not to be stored but are to be provided everytime the service has to be used.

By delegating identification to the **orchestration layer** we reduce the latency of each request by avoiding querying a central database for every request. If the service gets compromised direct access to personal information is avoided. By eliminating the process of identification the services can remain focused on serving complex requests

It is important to now know what type of authorization is needed to secure the services at scale

## 4. Types of Authorization

There are different types of permissions set in order to protect and restrict the usage of services. These perimssion types are broadly classified into the following categories:
1. Role Based Access Control (RBAC)
2. Attribute Based Access Control (ABAC)
3. Relationship Based Access Control (ReBAC)

### 4.1 Role Based Access Control (RBAC)
- The permission to access a service is assigned to a particular **role**. 
- Role represents a group of people instead of individually assigning permissions to users, services or devices.
- Assigning permissions to a role makes it easier to manage who has access as all it takes is assign the role to user, service or device.
- "**Editor**" and "**Viewer**" are examples of what a role can be.
- It is important to understand that as organizations group if the process of creating roles is not kept in check it would lead to creation of hyper specific roles making it harder to manage the access control. "**Editor-America-North-Finance**" is not a good role to be created as it is hyper specific.

### 4.2 Attribute Based Access Control (ABAC)
- The permission to access a particular service is not assigned a general role but instead to a particular **attribute** that the requestor needs to have in order to access the service.
- These are more granular in nature when compared to Roles.
- These are used in cases where risk of exposure of services to un-authorized services is very high.
- Few examples include IP address of the requester, location and time of request

### 4.3 Relation Based Access Control (ReBAC)
- These permissions are set based on the relationship of the requester and the service.
- Example of such relations include "Owner", "Co-Author"

We know what types of permissions are to be sent for authorization. We need to the best approach to do send these permissions

## 5. Permission Packaging Processes
There are 3 types of packaging processes when it comes to authorization of a request.
1. Session based authorization
2. Third party based authorization (OAuth)
3. JWT based authorization

### 5.1 Session based Authorization
- The state of permission is stored on a centralised database against an opaque unique popularly know as the session id and this session id is stored as cookies on the browser.
- Every time a request needs to be made to the AI/ML service server an additional call has to be made to the central database to fetch the state stored against the session id and then needs to be attached to the request before forwarding the request.
- This approach was used in the early days of web development but in the current situation where we want low latency scable services we should not opt for the type of authorization process.
 
### 5.2 Third Party based Authorization (OAuth)
- Identity and permission management happens on a centralised authorization server.
- In every call the service needs to call this authorization server to validate the token passed to it.
- The token used in this type of authorization is also **JWT** based.
- To avoid managing and re writing the code for identification and permission management developers often delegate the task to these third party applications.
- In this process data is not only sent outside it also increases the latency as communications have to be done with these centralized server every time to validate the token passed with the request

### 5.3 JWT based Authorization
- The servers do not need to **remember** the state every time a request is made. 
- All of the permissions (known as claims) are stored as one JSON which gets cryptographically signed as a token.
- At the service end the token will be checked if it has been altered and if it has been then the request will be invalidated.
- Even if the token gets compromised since a new token is created every time request is made and the token only contains permissions other credentials will not be exposed.

Out of the three process JWT based authorization should be here as it aligns with building scalable low latency services focused on AI/ML services

In order to implement JWT we need to understand how JWT works

## 6. Understanding JWT Authorization

### 6.1 What is JWT

JWT stands for JSON Web Token. It is an open standard that defines a compact and self contained way for securely transmitting information between 2 parties as JSON object

### 6.2 The structure of JWT

A JWT consists of 3 parts separated by a dot (`.`).
1. `header`: contains the type of token being used and the algorithm to created the signature. The JSON representing the header looks like `{"typ": "token", "alg": "HS256"}`
2. `payload`: contains the permissions called `claims`. The JSON representing the header looks like `{"name": "John Doe", "role": "admin", "sub": "1232123450}`
3. `signature`: It is used to verify that the sender is who they claim they are and ensures that the message has not been altered.
   
### 6.3 Flow of JWT creation

1. We create the `header` and `payload` JSON objects.
2. The `header` and `payload` JSON objects are converted into their `base64URL` strings (conversion using `base64URL` algorithm is to ensure that data is safe for transmission over the web as binary data. The output of `base64URl` is a string)
3. The encoded versions of `header` and `payload` are combined together but separated by a `dot`.
4. This combined encoded string is then signed using a symmetric/asymmetric algorithm using a secret key this is `signature` segment of the JWT token.
5. The encoded `header`, `payload` and the `signature` strings are combined together using a separator `.`. This entire string is the JWT `token` = `encodedHeader.encodedPayload.Signature`.
6. The token is added to the request as a header `Authorization: Bearer <token>`
7. This `Authorization` header acts as filter if the incoming request does not contain this header you should outright ignore the request is not a verifable request.

### 6.4 Flow of JWT verification

1. Once the request reaches the server you need to first verify it.
2. Check for the presence of the `Authorization` header if not present outright reject the request.
3. Extract the token from the `Authorization` header.
4. Split the `token` on `.` and store them into `encodedHeader`, `encodedPayload` and `incomingSignature` variables.
5. Combine the `encodedHeader`, `encodedPayload` with a `.` and encode it like how it was done when it was being created (for symmetric algorithm encoding you would need the same `secret key` used on the client end and for asymmetric algorithm encoding you should use the `public key` on client and `private key` on server for encoding).
6. Compare the new `signature` with the `incomingSignature` if they match then that means your request has not been modified and it is safe to move ahead with it.
7. If you want to use the permissions you can decode the `encodedPayload` to work with it.

**Note 1**: Remember that `base64URl` encoded string can be decoded by anyone. You can paste the it in jwt.io to decode it. It is just a measure to safely transfer strings over URL (making sure the data does not get corrupted while converting into binary packets of data for transfering over the web)

**Note 2**: If the secret key is exposed then the JWT can easily be hacked by changing the signature. Always import your secret key from secret managers.

### 6.5 JWT on Steroids
In a standard JWT the headers, payload and signature can still be decoded and hacked if the person performing the task is really good at its job. To go one step beyond JWT with higher level of security you can use **JWE**.

**JWE** stands for **JSON Web Encryption**. **JWE** encrypts content where as **JWT** only signs it.

JWE consists of 5 parts instead of 3:
1. `JOSE Header`: Contains information about the token and algorithm used. Equivalent of JWT `header`.
2. `JWE Encryption Key` (`JWE CEK`): The encrypted version of `Content Encryption Key`.
3. `Initialization Vector` (`IV`): A random sequence used to ensure the same data does not encryt the same request twice.
4. `Cipher Text`: The actual encrypted payload
5. `Authentication Tag`: Used to ensure integrity of the cipher text.
   

#### 6.5.1 JWE Token Creation Process
1. Random `Content Encryption Key` (`CEK`) is generated.
2. The `CEK` is again encrpted using the **symmetric** or **asymmetric** secret key and stored as `JWE CEK`.
3. The payload gets encrypted using the `CEK` and `IV` the algorithms used for encryption return the `Authentication Tag`.
4. All 5 parts are `base64URL` encoded.
5. They are joined together and stored into the `token` as `encodedHeader.encodedJWECEK.encodedIV.encodedCipherText.encodedAuthenticationTag`.
6. Add the token to the `Authorization` header.

#### 6.5.2 JWE Token Verification Process
1. Same initialization process of JWT is done for JWE regarding checking of the Authorization header and splitting of the token.
2. Using the **secret key** decode the `JWE CEK`.
3. Using the `IV` and the decrypted `JWE CEK` decrypt the `Cipher Text` and get the `Authentication Tag`.
4. Verify that the incoming `Authentication Tag` is same as the one created in step 3.
5. If it is the request can be worked on.
   
### 6.6 Why JWT over JWE
Even if JWE provides extra security where the payload and header cannot be decrypted without the secret key JWT should be **chosen** over JWE if you are not working for **Critical tasks** where exploitation of the token is **catastrophic**.

Here are the reasons why JWT should be used over JWE
1. **Computational Efficiency**: AI/ML inference is already compute-intensive. Standard JWT verification involves a simple hash-based signature check whereas JWE requires multiple layers of decryption
2. To validate the JWE token the server needs to perform descryptions twice in order to extract the payload
3. Verifcation of JWT takes **micro seconds** where as for JWE is **miliseconds**.

Here is an example with theoritical benchmarking.
We are trying to handle **10,000 concurrent requests**. Lets assume JWT signature check takes **100 microseconds (0.0001 seconds)** and JWE takes **1 milisecond** (0.001 seconds).
Then in one second using JWT verification we can achieve 1/0.0001 = **10,000** verifications per second per core where as for JWE it will be **1,000** verfications per second per core.

Even if we remove JSON parsing, context switching and network latency the speed of JWT verifcation is still 10 times that of JWE. Based on JWE's security features it is a good option to use instead of JWT but computationally its super expensive.

*If the Orchestration layer handles authentication and the traffic is encrypted via HTTPS why do the internal AI/ML services still need JWTs?*

The decision to implement JWTs at the service level is driven by three architectural necessities:
1. **Zero Trust Architecture**: We should not assume that the internal network is inherently "safe." If a single internal component is compromised an attacker could flood our AI services with requests. JWTs ensure that every single service verifies the caller's right to execute a workload regardless of where the request originated.
   
2. **Resource & Capital Protection**: AI/ML inference (especially with LLMs) is computationally expensive and carries a **high** "`cost-per-token`". Relying only on the orchestration layer for security is a high-risk strategy. A bypass at that layer could allow unauthorized users to drain the compute budget or "burn through capital" by overloading the server.

3. **Microservices Autonomy**: By requiring a JWT the AI service can perform its own rate-limiting and access control based on the claims ensuring the service remains resilient even if the gateway’s logic changes.

## 7 Conclusion

We will implement JWT-based Authorization for all AI/ML backend services. The Orchestration Layer will manage Authentication (identity verification), while the AI/ML Service Layer will perform local Authorization (permission enforcement) by validating signed JWT claims.

