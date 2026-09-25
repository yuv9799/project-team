'use client';
import './globals.css';
import Link from 'next/link';
import {Bell, Compass, FolderKanban, LogIn, Plus, UserCircle, Users, Sparkles} from 'lucide-react';
import {useEffect,useState} from 'react';

export default function RootLayout({children}:{children:React.ReactNode}){
 const [authed,setAuthed]=useState(false);
 useEffect(()=>{const sync=()=>setAuthed(!!localStorage.getItem('token'));sync();window.addEventListener('storage',sync);return()=>window.removeEventListener('storage',sync)},[]);
 return <html lang="en"><body>
  <header className="sticky top-0 z-40 border-b border-[#e7e9f2] bg-white/90 backdrop-blur-xl">
   <div className="section flex h-[68px] items-center justify-between">
    <Link href="/" className="flex items-center gap-2.5"><span className="flex h-9 w-9 items-center justify-center rounded-xl bg-[#5b5bd6] text-white shadow-lg shadow-[#5b5bd6]/20"><Users size={18}/></span><span className="text-[20px] font-black tracking-tight">Campus<span className="text-[#5b5bd6]">Connect</span></span></Link>
    <nav className="hidden items-center gap-7 md:flex"><Link className="nav-link" href="/discover">Discover</Link><Link className="nav-link" href="/projects/create">Create Project</Link><Link className="nav-link" href="/requests">Requests</Link><Link className="nav-link" href={authed?'/profile/me':'/login'}>Profile</Link></nav>
    <div className="flex items-center gap-2">{authed?<><Link href="/dashboard" className="hidden rounded-xl p-2.5 text-[#667085] hover:bg-[#f5f6fa] sm:block"><Bell size={19}/></Link><Link href="/profile/me" className="avatar h-9 w-9 text-sm">YC</Link></>:<><Link className="btn hidden sm:inline-flex" href="/login"><LogIn size={16}/>Login</Link><Link className="btn btn-primary" href="/register"><Plus size={16}/>Join</Link></>}</div>
   </div>
  </header>
  {children}
 </body></html>
}
