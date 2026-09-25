'use client';
import {useEffect,useState} from 'react';
import {useParams} from 'next/navigation';
import {api} from '../../../lib/api';
import Link from 'next/link';

export default function Profile(){
  const params = useParams();
  const id = params?.id as string;
  const [u,setU]=useState<any>(null);

  useEffect(()=>{
    if(id){
      api(`/api/users/${id}`).then(setU).catch(()=>{});
    }
  },[id]);

  if(!u)return <main className="section py-16"><div className="card p-10 text-center text-[#667085]">Loading profile...</div></main>;
  return <main><div className="section py-9"><div className="card overflow-hidden"><div className="h-32 bg-gradient-to-r from-[#5553c8] to-[#8a72ff]"/><div className="p-7"><div className="-mt-14 flex flex-col gap-5 sm:flex-row sm:items-end"><div className="avatar h-24 w-24 border-4 border-white text-2xl shadow-lg">{u.name?.split(' ').map((x:string)=>x[0]).join('').slice(0,2)}</div><div className="flex-1"><h1 className="text-3xl font-black">{u.name}</h1><p className="mt-1 text-[#667085]">{u.branch} · Year {u.year} · {u.college}</p></div><Link href="/discover" className="btn">Back to discover</Link></div><p className="mt-6 max-w-3xl leading-7 text-[#667085]">{u.bio||'Student collaborator looking for interesting projects and people to build with.'}</p><div className="mt-6 flex flex-wrap gap-2">{u.skills?.map((s:any)=><span className="pill" key={s.id}>{s.name}</span>)}</div></div></div></div></main>
}

