import Navbar from "@/components/Navbar";

export default function Layout({ children }: Readonly<{ children: React.ReactNode }>) {
    return (
        <div className=" mx-auto">
        <header className="">
            <Navbar />
        </header>
        <main>{children}</main>
        <footer className="py-4">Footer Content</footer>
      </div>
    )
}