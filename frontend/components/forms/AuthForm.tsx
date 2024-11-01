/* eslint-disable @typescript-eslint/no-unused-vars */
/* eslint-disable react/no-unescaped-entities */
"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import Link from "next/link";
import {
  DefaultValues,
  FieldValues,
  Path,
  SubmitHandler,
  useForm,
} from "react-hook-form";
import { z, ZodType } from "zod";
import { useRouter } from 'next/navigation';

import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import ROUTES from "@/constants/routes";


interface AuthFormProps<T extends FieldValues> {
  schema: ZodType<T>;
  defaultValues: T;
  formType: "SIGN_IN" | "SIGN_UP";
}

const AuthForm = <T extends FieldValues>({
  schema,
  defaultValues,
  formType,
}: AuthFormProps<T>) => {
  const form = useForm<z.infer<typeof schema>>({
    resolver: zodResolver(schema),
    defaultValues: defaultValues as DefaultValues<T>,
  });
  const router = useRouter(); // Initialize the router

  const handleSubmit: SubmitHandler<T> = async (data) => {
    
    const response = await fetch("http://localhost:8001/api/users/login", {
        
        method: "POST",
        headers: {
        "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
});
console.log(response);

    if (response.ok) {
      const result = await response.json();
      localStorage.setItem("accessToken", result.access); // Store the token
      localStorage.setItem("username", data.username); // Store the username
      router.push("/"); // Redirect to the home page
    } else {
      const errorData = await response.json();
      console.error("Login failed:", errorData); // Handle error (show message to user)
    }
  };

  const buttonText = formType === "SIGN_IN" ? "Sign In" : "Sign Up";

  return (
    <Form {...form}>
      <form
        onSubmit={form.handleSubmit(handleSubmit)}
        className="mt-10 space-y-6"
      >
        {Object.keys(defaultValues).map((field) => (
          <FormField
            key={field}
            control={form.control}
            name={field as Path<T>}
            render={({ field }) => (
              <FormItem className="flex flex-col gap-2">
                <FormLabel className="text-gray-700 font-medium">
                  {field.name === "username"
                    ? "Username"
                    : field.name.charAt(0).toUpperCase() + field.name.slice(1)}
                </FormLabel>
                <FormControl>
                  <Input
                    required
                    type={field.name === "password" ? "password" : "text"}
                    {...field}
                    className="border-gray-300 rounded-md shadow-sm focus:ring focus:ring-blue-500 focus:border-blue-500"
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        ))}

        <Button
          disabled={form.formState.isSubmitting}
          className="w-full bg-blue-600 text-white py-3 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 transition duration-200"
        >
          {form.formState.isSubmitting
            ? "Signing In..."
            : buttonText}
        </Button>

        <p className="text-center">
          <Link
            href={ROUTES.SIGN_UP}
            className="text-blue-600 font-semibold hover:underline"
          >
            Don't have an account? Sign up
          </Link>
        </p>
      </form>
    </Form>
  );
};

export default AuthForm;
