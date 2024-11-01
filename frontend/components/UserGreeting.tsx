import Link from "next/link";
import Image from "next/image";
import { useEffect, useState } from "react";
import ROUTES from "@/constants/routes";

const UserGreeting = () => {
  const [username, setUsername] = useState<string | null>(null);

  useEffect(() => {
    if (typeof window !== "undefined") {
      const storedUsername = localStorage.getItem("username");
      setUsername(storedUsername);
    }
  }, []);

  const handleLogout = () => {
    // Clear username from localStorage
    localStorage.removeItem("username");
    setUsername(null);
    // Optionally redirect or show a logout message
    window.location.href = ROUTES.SIGN_IN; // Redirect to login page after logout
  };

  return (
    <div className="flex items-center">
      {username ? (
        <div className="flex items-center space-x-2">
          <span className="text-gray-700">Welcome, {username}!</span>
          <span
            onClick={handleLogout}
            className="bg-red-500 text-white p-2  rounded"
          >
            Logout
          </span>
        </div>
      ) : (
        <Link href={ROUTES.SIGN_IN} className="flex items-center">
          <Image
            src="/icons/account.svg"
            alt="Account"
            width={20}
            height={20}
            className="invert-colors lg:hidden"
          />
          <span className="primary-text-gradient max-lg:hidden">Log In</span>
        </Link>
      )}
    </div>
  );
};

export default UserGreeting;
