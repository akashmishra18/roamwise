export const destinations = [
 {name:'Kyoto',country:'Japan',tag:'Culture & quiet moments',image:'photo-1493976040374-85c8e12f0c0e',color:'#d7e2d1'},
 {name:'Bali',country:'Indonesia',tag:'A little closer to paradise',image:'photo-1537996194471-e657df975ab4',color:'#c8dfd9'},
 {name:'Paris',country:'France',tag:'Fall in love with the everyday',image:'photo-1502602898657-3e91760cbb34',color:'#ded5ce'},
 {name:'Rome',country:'Italy',tag:'Stories around every corner',image:'photo-1552832230-c0197dd311b5',color:'#ded4c0'}
];
export const photo = (id,w=900)=>`https://images.unsplash.com/${id}?auto=format&fit=crop&w=${w}&q=85`;
export const initialPreferences={destination:'Kyoto, Japan',start_date:'2026-11-13',end_date:'2026-11-15',budget:900,currency:'USD',group_size:1,style:'Balanced',interests:['Culture','Food'],notes:''};
export function demoPlan(p,revision=0){
 const count=Math.round((new Date(p.end_date)-new Date(p.start_date))/86400000)+1;
 const city=p.destination.split(',')[0];
 const themes=[...p.interests,'Neighborhood discoveries','Local favorites'];
 return {title:`A little escape to ${city}`,summary:`A ${p.style.toLowerCase()} journey for ${p.group_size}, with time for ${p.interests.join(', ').toLowerCase()} and the unexpected.`,source:'demo',days:Array.from({length:count},(_,i)=>({day:i+1,title:themes[(i+revision)%themes.length],activities:[
 {time:'09:00',title:revision%2?'A slow start in a local café':'Breakfast & a neighborhood stroll',category:'Dining',description:`Find a café near your stay in ${city}. Leave time to settle into the neighborhood.`,duration:90,cost:Math.round(p.budget/count*.07),location:`Central ${city}`},
 {time:'11:00',title:`Explore ${themes[(i+revision)%themes.length].toLowerCase()}`,category:'Attraction',description:'Choose a nearby highlight that fits your interests. Confirm opening hours and tickets before heading out.',duration:p.style==='Relaxed'?120:150,cost:Math.round(p.budget/count*.12),location:`${city} city center`},
 {time:'14:00',title:'A taste of the local scene',category:'Dining',description:'Pause for lunch at a neighborhood restaurant. Ask about seasonal specialties and dietary options.',duration:90,cost:Math.round(p.budget/count*.1),location:`Central ${city}`},
 ...(p.style==='Relaxed'?[]:[{time:'16:00',title:revision%2?'Discover a different neighborhood':'An afternoon of small discoveries',category:'Attraction',description:'Explore nearby streets and independent shops, with a break whenever you need one.',duration:120,cost:Math.round(p.budget/count*.08),location:`Central ${city}`}]),
 {time:'19:00',title:'Dinner, then take the scenic way home',category:'Dining',description:'End the day with a relaxed dinner close to your accommodation.',duration:90,cost:Math.round(p.budget/count*.12),location:`Central ${city}`}
 ],accommodation:{name:p.style==='Luxury'?'Boutique hotel suggestion':'Central guesthouse suggestion',cost:Math.round(p.budget/count*.3)},transport:{description:'Walk between nearby stops; use local transit for longer journeys.',cost:Math.round(p.budget/count*.08)}}))};
}
export const totalCost=trip=>trip.days.reduce((s,d)=>s+d.activities.reduce((a,b)=>a+Number(b.cost),0)+Number(d.accommodation.cost)+Number(d.transport.cost),0);
