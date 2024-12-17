import dynamic from "next/dynamic";

const LeafletMap = dynamic(() => import("./LeafletMap"), { ssr: false });

const Page = () => {
  return <div style={{width:"100%", height:"100vh", overflow:"hidden"}}>
    <LeafletMap />
  </div>
};

export default Page;
