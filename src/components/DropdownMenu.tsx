import type React from 'react';
import { Fragment } from 'react';
import { BsThreeDotsVertical } from 'react-icons/bs';
import { Menu, Transition } from '@headlessui/react';

const DropdownMenu: React.FC = () => {
  return (
    <>
      <Menu>
        <Menu.Button className="hover:text-primary text-xl pl-2 md:hidden">
          <BsThreeDotsVertical />
        </Menu.Button>
        <Transition
          as={Fragment}
          enter="transition ease-out duration-100"
          enterFrom="transform opacity-0 scale-95"
          enterTo="transform opacity-100 scale-100"
          leave="transition ease-in duration-75"
          leaveFrom="transform opacity-100 scale-100"
          leaveTo="transform opacity-0 scale-95"
        >
          <Menu.Items className="absolute right-0 mt-2 w-56 origin-top-right divide-y divide-gray-100 rounded-md bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
            <Menu.Item>
              <button>Home</button>
            </Menu.Item>
          </Menu.Items>
        </Transition>
      </Menu>
    </>
  );
};

export default DropdownMenu;
