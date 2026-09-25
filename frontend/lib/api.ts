const API=process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
export function token(){if(typeof window==='undefined')return '';return localStorage.getItem('token')||''}
export async function api<T=any>(path:string, options:RequestInit={}){const headers=new Headers(options.headers);headers.set('Content-Type','application/json');const t=token();if(t)headers.set('Authorization',`Bearer ${t}`);const r=await fetch(`${API}${path}`,{...options,headers,cache:'no-store'});if(!r.ok){let e:any={};try{e=await r.json()}catch{};throw new Error(e.detail||'Request failed')}return r.json() as Promise<T>}
export function saveAuth(data:any){localStorage.setItem('token',data.access_token);localStorage.setItem('user',JSON.stringify(data.user))}
