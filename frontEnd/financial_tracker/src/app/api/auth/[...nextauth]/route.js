import NextAuth from "next-auth";
import CredentialsProvider from "next-auth/providers/credentials";
import { authenticateUser } from "@/lib/auth"; // Import the helper function


export const authOptions = {
  providers: [
    CredentialsProvider({
      async authorize(credentials) {
        return authenticateUser(credentials); // Call the helper function
      }
    })
  ],
  session: { strategy: "jwt" },
};

const handler = NextAuth(authOptions);
export { handler as GET, handler as POST };