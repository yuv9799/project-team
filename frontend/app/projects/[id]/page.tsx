'use client';
import {useEffect,useState} from 'react';
import {useParams} from 'next/navigation';
import Link from 'next/link';
import {api} from '../../../lib/api';
import {Users,Clock3,Sparkles} from 'lucide-react';

export default function Project(){
  const params = useParams();
  const id = params?.id as string;
  const [p,setP]=useState<any>(null), [matches,setMatches]=useState<any[]>([]), [error,setError]=useState('');

  useEffect(()=>{
    if(id){
      api(`/api/projects/${id}`).then(setP).catch(e=>setError(e.message));
      api(`/api/projects/${id}/recommendations`).then(setMatches).catch(()=>{});
    }
  },[id]);

  if(error)return <main className="section py-16"><div className="card p-10 text-center">{error}</div></main>;
  if(!p)return <main className="section py-16"><div className="card p-10">Loading project...</div></main>;
  return <main><div className="section py-9"><div className="grid gap-5 lg:grid-cols-[1fr_360px]"><div className="card p-7"><span className="pill">{p.category}</span><h1 className="mt-4 text-4xl font-black">{p.name}</h1><p className="mt-3 max-w-3xl leading-7 text-[#667085]">{p.description}</p><div className="mt-6 flex flex-wrap gap-2">{p.skills?.map((s:any)=><span className="pill pill-gray" key={s.id}>{s.name}</span>)}</div><div className="mt-7 grid gap-3 sm:grid-cols-3"><div className="rounded-2xl bg-[#f8f9fc] p-4"><Users size={18} className="text-[#5b5bd6]"/><div className="mt-2 text-sm text-[#667085]">Team</div><div className="font-black">{p.members?.length||1}/{p.team_size}</div></div><div className="rounded-2xl bg-[#f8f9fc] p-4"><Clock3 size={18} className="text-[#12b76a]"/><div className="mt-2 text-sm text-[#667085]">Duration</div><div className="font-black">{p.duration_weeks} weeks</div></div><div className="rounded-2xl bg-[#f8f9fc] p-4"><Sparkles size={18} className="text-[#f79009]"/><div className="mt-2 text-sm text-[#667085]">Matching</div><div className="font-black">AI-ready</div></div></div></div><aside className="card p-6"><div className="font-black">Recommended teammates</div><p className="mt-1 text-sm text-[#667085]">People who can fill the project's skill gaps.</p><div className="mt-5 space-y-3">{matches.slice(0,5).map((m:any)=><div className="rounded-2xl border border-[#eef0f5] p-4" key={m.user.id}><div className="flex items-center gap-3"><div className="avatar h-10 w-10">{m.user.name?.split(' ').map((x:string)=>x[0]).join('').slice(0,2)}</div><div className="flex-1"><div className="font-bold">{m.user.name}</div><div className="text-xs text-[#667085]">{m.user.skills?.slice(0,2).map((s:any)=>s.name).join(' · ')}</div></div><div className="font-black text-[#5b5bd6]">{m.score}%</div></div></div>)}{matches.length===0&&<div className="rounded-2xl bg-[#f8f9fc] p-4 text-sm text-[#667085]">Sign in and add more profile details to get personalized recommendations.</div>}</div><Link href="/discover" className="btn btn-primary mt-5 w-full">Find more teammates</Link></aside></div></div></main>
}

