import {Routes,Route,Navigate} from 'react-router-dom';
import ProtectedRoute from '../auth/ProtectedRoute';
import Landing from '../features/public/Landing';
import RoleSelection from '../features/role-selection/RoleSelection';
import {Login,Signup} from '../features/auth/AuthPages';
import CitizenDashboard,{RequestDetail} from '../features/citizen/CitizenDashboard';
import ReportNeed from '../features/citizen/ReportNeed';
import VolunteerDashboard from '../features/volunteer/VolunteerDashboard';
import VerifyNeed from '../features/volunteer/VerifyNeed';
import PlannerDashboard from '../features/planner/PlannerDashboard';
import Accountability from '../features/planner/Accountability';
import AdminDashboard from '../features/admin/AdminDashboard';
import AIOpsDashboard from '../features/admin/AIOpsDashboard';
const protect=(roles,element)=><ProtectedRoute allowedRoles={roles}>{element}</ProtectedRoute>;
const reporters=['citizen','volunteer'];
export default function AppRoutes(){return <Routes>
 <Route path="/" element={<Landing/>}/><Route path="/auth/role" element={<RoleSelection/>}/>
 <Route path="/auth/login" element={<Login/>}/><Route path="/admin/login" element={<Login admin/>}/>
 <Route path="/auth/signup/citizen" element={<Signup/>}/><Route path="/auth/signup/volunteer" element={<Signup kind="volunteer"/>}/><Route path="/auth/access-request" element={<Signup kind="official"/>}/>
 <Route path="/citizen" element={protect(reporters,<CitizenDashboard/>)}/>
 {['/citizen/capture','/citizen/add-location','/citizen/capture-evidence','/citizen/report-need','/volunteer/capture'].map(path=><Route key={path} path={path} element={protect(reporters,<ReportNeed/>)}/>)}
 {['/citizen/requests/:id','/volunteer/requests/:id'].map(path=><Route key={path} path={path} element={protect(reporters,<RequestDetail/>)}/>)}
 <Route path="/volunteer" element={protect(['volunteer'],<VolunteerDashboard/>)}/>
 <Route path="/volunteer/requests" element={protect(['volunteer'],<CitizenDashboard/>)}/>
 <Route path="/volunteer/verify/:id" element={protect(['volunteer'],<VerifyNeed/>)}/>
 {['district','state','national'].map((level,i)=><Route key={level} path={'/dashboard/'+level} element={protect([['district_official','state_planner','national_planner'][i]],<PlannerDashboard level={level}/>)}/>)}
 <Route path="/accountability/*" element={<Accountability/>}/>
 <Route path="/admin" element={protect(['admin'],<AdminDashboard/>)}/>
 <Route path="/admin/ai-ops" element={protect(['admin','auditor'],<AIOpsDashboard/>)}/>
 <Route path="*" element={<Navigate to="/" replace/>}/>
 </Routes>;}
