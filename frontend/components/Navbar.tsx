// components/Navbar.js
'use client'
import Link from 'next/link';
import { useState } from 'react';
import UserGreeting from './UserGreeting';

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  return (
    <header className="flex whitespace-nowrap items-center justify-between border-b border-solid border-[#e0e4e7] px-2 py-3 md:px-7 bg-white shadow-sm">
      {/* Logo and Title */}
        <Link href={'/'}  className='px-2'>
      <div className="flex items-center gap-2 text-[#111517]">
        <div className="w-7 h-7 flex items-center justify-center rounded-full bg-[#2c99e2] hover:scale-110 transition-transform duration-200">
          <svg className="w-6 h-6 text-white" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path
              d="M36.7273 44C33.9891 44 31.6043 39.8386 30.3636 33.69C29.123 39.8386 26.7382 44 24 44C21.2618 44 18.877 39.8386 17.6364 33.69C16.3957 39.8386 14.0109 44 11.2727 44C7.25611 44 4 35.0457 4 24C4 12.9543 7.25611 4 11.2727 4C14.0109 4 16.3957 8.16144 17.6364 14.31C18.877 8.16144 21.2618 4 24 4C26.7382 4 29.123 8.16144 30.3636 14.31C31.6043 8.16144 33.9891 4 36.7273 4C40.7439 4 44 12.9543 44 24C44 35.0457 40.7439 44 36.7273 44Z"
              fill="currentColor"
            />
          </svg>
        </div>
        <h2 className="text-lg font-semibold">Healthcare</h2>
      </div>
        </Link>

      {/* Desktop Nav */}
      <div className="hidden md:flex flex-1 justify-end items-center gap-2">
        <nav className="flex items-center gap-5 lg:gap-6">
          {['Dashboard', 'Order History', 'Inventory', 'Suppliers', 'Reports', 'Settings'].map((item) => (
            <Link key={item} href={`/${item.toLowerCase().replace(' ', '-')}`}>
              <span className="text-[#111517] text-sm font-medium hover:text-[#2c99e2] transition-colors duration-200">{item}</span>
            </Link>
          ))}
        </nav>
          <UserGreeting />
          </div>

      {/* Mobile Menu Button */}
      <button
        className="md:hidden flex items-center justify-center text-[#111517] focus:outline-none"
        onClick={() => setIsMenuOpen(!isMenuOpen)}
        aria-label="Toggle menu"
      >

        <svg className="w-6 h-6 text-gray-800 dark:text-white" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" viewBox="0 0 24 24">
          {isMenuOpen ? (
            <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M18 6H6m12 4H6m12 4H6m12 4H6" />
          ) : (
            <path stroke="currentColor" strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M18 6H6m12 4H6m12 4H6m12 4H6" />
          )}
        </svg>
      </button>

      {/* Mobile Nav */}
      {isMenuOpen && (
        <div className="absolute top-16 left-0 w-full bg-white shadow-md md:hidden transition-all duration-300 ease-in-out transform origin-top">
          <nav className="flex flex-col items-center gap-4 py-4">
            {['Dashboard', 'Order-History', 'Inventory', 'Suppliers', 'Reports', 'Settings'].map((item) => (
              <Link key={item} href={`/${item.toLowerCase().replace(' ', '-')}`}>
                <span className="text-[#111517] text-base font-medium hover:text-[#2c99e2] transition-colors duration-200">{item}</span>
              </Link>
              
            ))}
          <UserGreeting />

          </nav>
          
        </div>
      )}
    </header>
  );
};

export default Navbar;
