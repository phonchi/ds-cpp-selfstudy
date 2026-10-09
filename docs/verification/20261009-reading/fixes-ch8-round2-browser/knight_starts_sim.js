const knightMoves=[[-1,-2],[-1,2],[-2,-1],[-2,1],[1,-2],[1,2],[2,-1],[2,1]];
function legal(r,c,n,v){const o=[];for(const[dr,dc]of knightMoves){const a=r+dr,b=c+dc;if(a>=0&&a<n&&b>=0&&b<n&&!v[a][b])o.push([a,b]);}return o;}
function solve(n,sr,sc,heur,LIMIT=800000){const v=Array.from({length:n},()=>Array(n).fill(false));v[sr][sc]=true;let steps=1,back=0,ab=false;const T=n*n;
const dfs=(r,c,d)=>{if(ab)return false;if(steps>LIMIT){ab=true;return false;}if(d===T)return true;let m=legal(r,c,n,v);
if(heur){m=m.map(([a,b])=>{let k=0;for(const[dr,dc]of knightMoves){const x=a+dr,y=b+dc;if(x>=0&&x<n&&y>=0&&y<n&&!v[x][y]&&!(x===r&&y===c))k++;}return{a,b,k}}).sort((p,q)=>p.k-q.k).map(z=>[z.a,z.b]);}
else m.sort((p,q)=>(p[0]*100+p[1])-(q[0]*100+q[1]));
for(const[a,b]of m){v[a][b]=true;steps++;if(dfs(a,b,d+1))return true;v[a][b]=false;back++;steps++;}return false;};
const ok=dfs(sr,sc,1);return {ok,ab,steps,back};}
for(const n of [5,6,7,8]){for(let r=0;r<n;r++)for(let c=0;c<n;c++){if(c<r||r>Math.floor((n-1)/2))continue; // symmetry-reduced
 const h=solve(n,r,c,true),p=solve(n,r,c,false);console.log(n,`(${r},${c})`,(r+c)%2?'odd':'even','W:',h.ok?'ok':(h.ab?'ABORT':'fail'),h.steps,h.back,' plain:',p.ok?'ok':(p.ab?'ABORT':'fail'),p.steps,p.back);}}
