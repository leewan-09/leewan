import type React from 'react';
import { Fragment } from 'react';
import { BsThreeDotsVertical } from 'react-icons/bs/index';
import { Menu, Transition } from '@headlessui/react';

const DropdownMenu: React.FC = () => {
  return (
    <div className="md:hidden">
      <Menu>
        <Menu.Button
          className="hover:text-primary text-2xl pl-2 focus:outline-none outline-none"
          aria-label="Menu">
          <BsThreeDotsVertical />
        </Menu.Button>
        <Transition
          as={Fragment}
          enter="transition ease-out duration-100"
          enterFrom="transform opacity-0 scale-95"
          enterTo="transform opacity-100 scale-100"
          leave="transition ease-in duration-75"
          leaveFrom="transform opacity-100 scale-100"
          leaveTo="transform opacity-0 scale-95">
          <Menu.Items className="absolute bg-zinc-700 right-6  w-40 origin-top-right rounded-md shadow-xl ring-1 ring-black ring-opacity-5 focus:outline-none">
            <div className="p-2">
              <Menu.Item>
                <button className="hover:text-primary transition-colors text-left w-full text-sm p-1">
                  About me
                </button>
              </Menu.Item>
              <Menu.Item>
                <a
                  href="https://leewan-09.showwcase.com/shows"
                  className="hover:text-primary transition-colors text-left w-full text-sm p-1">
                  Showcase
                </a>
              </Menu.Item>
            </div>
          </Menu.Items>
        </Transition>
      </Menu>
    </div>
  );
};

export default DropdownMenu;
