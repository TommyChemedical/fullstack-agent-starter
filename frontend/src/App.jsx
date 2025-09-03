import HealthCard from './components/HealthCard';
import AgentRun from './components/AgentRun';
import GitInfo from './components/GitInfo';
import OpenPRForm from './components/OpenPRForm';
import TelemetryCard from './components/TelemetryCard';

export default function App(){
  return (
    <div className="max-w-5xl mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-bold">Agent Control Panel</h1>
      <HealthCard />
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <AgentRun />
        <GitInfo />
      </div>
      <OpenPRForm />
      <TelemetryCard />
    </div>
  );
}