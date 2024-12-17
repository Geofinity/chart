import dynamic from "next/dynamic";

const LeafletMap = dynamic(() => import("../(main)/uikit/maps/LeafletMap.js"), { ssr: false });

const Page = () => {
  return <div style={{width:"100%", height:"100%", overflow:"hidden"}}>
    <LeafletMap />
  </div>
};

export default Page;
