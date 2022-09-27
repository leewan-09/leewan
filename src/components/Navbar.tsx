import type React from 'react';
import {
  AiFillGithub,
  AiFillLinkedin,
  AiOutlineTwitter,
} from 'react-icons/ai/index';
import DropdownMenu from './DropdownMenu';

const Navbar: React.FC = () => {
  return (
    <nav className="max-w-screen-xl w-full h-14 m-auto px-6">
      <div className="flex h-full justify-between items-center">
        <div className="flex text-xl font-semibold tracking-wider group cursor-pointer">
          <div className="flex flex-col">
            <div className="group-hover:text-primary transition-all ease-in-out">
              LEE
            </div>
            <div className="h-[2px] bg-primary group-hover:bg-white transition-all ease-in-out"></div>
          </div>
          <div className="flex flex-col">
            <div className="text-primary  group-hover:text-white transition-all ease-in-out">
              WAN
            </div>
            <div className="h-[2px] bg-white group-hover:bg-primary transition-all ease-in-out"></div>
          </div>
        </div>
        <div className="text-sm hidden md:flex">
          <a
            href="/"
            className="px-2 md:px-5 hover:text-primary transition-colors"
          >
            Home
          </a>
          <a
            href="/"
            className="px-2 md:px-5 hover:text-primary transition-colors"
          >
            About me
          </a>
          <a
            href="/"
            className="px-2 md:px-5 hover:text-primary transition-colors"
          >
            Showcase
          </a>
        </div>
        <div>
          <div className="flex">
            <a
              href="https://github.com/leewan-09"
              target="_blank"
              className="pr-2"
            >
              <AiFillGithub className="hover:text-primary transition-colors text-xl" />
            </a>
            <a
              href="https://twitter.com/leewan98"
              target="_blank"
              className="px-2"
            >
              <AiOutlineTwitter className="hover:text-primary transition-colors text-xl" />
            </a>
            <a
              href="https://www.linkedin.com/in/ahmed-leevan-b02b91240/"
              target="_blank"
              className="md:px-2 pl-2"
            >
              <AiFillLinkedin className="hover:text-primary transition-colors text-xl" />
            </a>

            <DropdownMenu />
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
