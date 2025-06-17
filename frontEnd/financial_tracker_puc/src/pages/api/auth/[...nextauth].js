"use client";
import NextAuth from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";

import axios from "axios";


export default NextAuth({
  providers: [
    CredentialsProvider({
      name: "Credentials",
      credentials: {
        username: { label: "Username", type: "text" },
        password: { label: "Password", type: "password" },
      },
      async authorize(credentials) {
        //const user =  await authenticateUser(credentials); // Call the helper function
        
        const request_json = JSON.stringify({
          email: credentials.email,
          password: credentials.password,
        });
        
        const request_headers = {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Access-Control-Allow-Origin': "*",
          'Access-Control-Allow-Credentials': 'true'};
        
        const https = require('https');

          // Make the API request
        const response  = await axios.post(`${process.env.NEXT_PUBLIC_API_URL}/auth`, request_json, {withCredentials: true, 
                                                                                                     headers: request_headers,
                                                                                                     timeout: 5000,
                                                                                                     httpsAgent: new https.Agent({ rejectUnauthorized: false })});

          
        const user = response.data;
        const jwt_token = response.headers["set-cookie"]//[0].split(';')[0].split('=')[1]; // Extract the JWT token from the response headers
        user.jwt_token = jwt_token; // Add the JWT token to the user object        
        //console.log("User:", user);
        //console.log("Token:", jwt_token);

         // Check if user is valid
        if (!user) {
          throw new Error("Invalid credentials");
        } else {
          return {
            id: user.user_id,
            first_name: user.first_name,
            last_name: user.last_name,
            email: user.email, 
            role: "user",
            jwt_token: jwt_token,
          };
        } 
      },
    }),
  ],
  session: {
    strategy: "jwt",
  },
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        //token.jwt = user.token;
        token.jwt = user.jwt_token; // Use the jwt_token from the user object
        token.id = user.id;
        token.first_name = user.first_name;
        token.last_name = user.last_name;
        token.email = user.email;
        token.role = user.role;
      }
      return token;
    },
    async session({ session, token  }) {
      //session.jwt = token.jwt;
      session.user.jwt = token.jwt;
      session.user.id = token.id;
      session.user.first_name = token.first_name;
      session.user.last_name = token.last_name;
      session.user.email = token.email;
      session.user.role = token.role;
      return session;
    },
  },
  secret: process.env.NEXTAUTH_SECRET,
});
