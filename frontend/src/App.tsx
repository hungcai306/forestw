import {useState} from 'react';
import MapPanel from './components/MapPanel';
import {api} from './services/api';
import './styles.css';

type User={full_name:string;role:string;admin_username:string;email?:string|null};
export default function App(){
 const [adminUsername,setAdminUsername]=useState('sadmin'); const [password,setPassword]=useState('ChangeMe123!');
 const [user,setUser]=useState<User|null>(null); const [error,setError]=useState('');
 async function login(){try{const {data}=await api.post('/auth/login',{admin_username:adminUsername,password});localStorage.setItem('token',data.access_token);setUser(data.user);setError('');}catch(e:any){setError(e.response?.data?.detail||'Không đăng nhập được');}}
 if(!user) return <main className="login"><section><h1>Hue ForestWatch</h1><p>Giám sát biến động rừng và quản trị phân quyền</p><input value={adminUsername} onChange={e=>setAdminUsername(e.target.value)} placeholder="Tên đăng nhập" autoComplete="username"/><input type="password" value={password} onChange={e=>setPassword(e.target.value)} placeholder="Mật khẩu" autoComplete="current-password"/><button onClick={login}>Đăng nhập</button>{error&&<small>{error}</small>}</section></main>;
 return <div className="layout"><aside><h2>ForestWatch</h2><div className="profile"><b>{user.full_name}</b><span>{user.admin_username} · {user.role}</span></div><nav><button>Tổng quan</button><button>Bản đồ so sánh</button><button>Cảnh báo</button><button>Tài khoản</button><button>Nhóm & Trạm</button><button>Phân quyền địa bàn</button><button>Báo cáo</button><button>Nhật ký</button></nav></aside><main><header><div><h1>Bản đồ so sánh rừng</h1><p>Rừng tự nhiên · Rừng trồng · Chính quyền địa phương 2 cấp</p></div><button onClick={()=>{localStorage.removeItem('token');setUser(null)}}>Đăng xuất</button></header><section className="toolbar"><label>Lớp T1<input type="date"/></label><label>Lớp T2<input type="date"/></label><label>Loại rừng<select><option>Tất cả</option><option>Rừng tự nhiên</option><option>Rừng trồng</option></select></label><button>Chạy so sánh</button><button>Xuất PDF</button></section><section className="cards"><article><span>Mất rừng tự nhiên</span><strong>0,00 ha</strong></article><article><span>Mất rừng trồng</span><strong>0,00 ha</strong></article><article><span>Tự nhiên → trồng</span><strong>0,00 ha</strong></article><article><span>Cảnh báo chờ xử lý</span><strong>0</strong></article></section><MapPanel/></main></div>;
}
