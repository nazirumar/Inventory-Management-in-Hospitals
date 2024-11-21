

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className='text-center'
      >
        {children}
      </body>
    </html>
  );
}
