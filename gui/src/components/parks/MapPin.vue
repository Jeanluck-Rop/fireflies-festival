<script lang="ts">
 import L from 'leaflet'
 import type { Parque } from '../../stores/parks'
 
 export function isParkOpen(park: Parque): boolean {
   if (!park.activo)
     return false
   
   const apertura = park.horario_apertura
   const cierre = park.horario_cierre
   
   if (apertura === cierre || (apertura === '00:00' && cierre === '00:00'))
     return true
   
   const offsetHours = Math.round(park.longitud / 15)
   const nowUtc = new Date()
   const parkTime = new Date(nowUtc.getTime() + offsetHours * 60 * 60 * 1000)
   const parkMinutes = parkTime.getUTCHours() * 60 + parkTime.getUTCMinutes()
   
   const [aH, aM] = apertura.split(':').map(Number)
   const [cH, cM] = cierre.split(':').map(Number)
   const openMinutes  = aH * 60 + aM
   const closeMinutes = cH * 60 + cM

   if (openMinutes > closeMinutes)
     return parkMinutes >= openMinutes || parkMinutes < closeMinutes
   return parkMinutes >= openMinutes && parkMinutes < closeMinutes
 }

 //Diseno del pin
 export function createPinIcon(park: Parque, open: boolean): L.DivIcon {
   const accent = '#E8FF7A'

   const glow = open
	      ? `filter: drop-shadow(0 0 6px rgba(232,255,122,0.9)) drop-shadow(0 0 16px rgba(232,255,122,0.4));`
	      : `filter: grayscale(1) brightness(0.35);`

   const pulse = open
	       ? `<style>
                   @keyframes ff-pin-pulse { 0%, 100%
                                             { opacity: 0.75; transform: scale(1) }
                                             50%
                                             { opacity: 1; transform: scale(1.08) }
                                           }
                        </style>` : ''

   const animation = open
		   ? `animation: ff-pin-pulse 3s ease-in-out infinite;`
		   : ''

   const svg =
     `<div style="width:48px;height:64px;display:flex;align-items:flex-start;justify-content:center;">
      <svg viewBox="0 0 40 52" width="48" height="64" fill="none"
        style="${glow} ${animation}"
        xmlns="http://www.w3.org/2000/svg">
        ${pulse}
        <ellipse cx="20" cy="50" rx="5" ry="2" fill="rgba(0,0,0,0.3)"/>
        <path d="M20 50 L13 28 Q20 32 27 28 Z"
          fill="${accent}" fill-opacity="${open ? '0.9' : '0.4'}"/>
        <circle cx="20" cy="18" r="16" fill="#0d1a10"
          stroke="${accent}" stroke-width="1.5"
          stroke-opacity="${open ? '0.8' : '0.3'}"/>
        ${open ? `<circle cx="20" cy="18" r="14" fill="${accent}" fill-opacity="0.06"/>` : ''}
        <ellipse cx="13" cy="15" rx="4.5" ry="2.5"
          fill="${accent}" fill-opacity="0.35" transform="rotate(-25 13 15)"/>
        <ellipse cx="27" cy="15" rx="4.5" ry="2.5"
          fill="${accent}" fill-opacity="0.35" transform="rotate(25 27 15)"/>
        <ellipse cx="20" cy="19" rx="3.5" ry="6"
          fill="#161D1A" stroke="${accent}" stroke-width="1.1"/>
        <ellipse cx="20" cy="24" rx="2.2" ry="2.5"
          fill="#F4FFA0" fill-opacity="${open ? '1' : '0.2'}"/>
        <ellipse cx="20" cy="24" rx="1.2" ry="1.5"
          fill="#FFFDE8" fill-opacity="${open ? '1' : '0.2'}"/>
        <path d="M18 13 Q16 10 14 11"
          stroke="${accent}" stroke-width="0.9"
          stroke-linecap="round" stroke-opacity="0.8"/>
        <path d="M22 13 Q24 10 26 11"
          stroke="${accent}" stroke-width="0.9"
          stroke-linecap="round" stroke-opacity="0.8"/>
      </svg>
    </div>`

   return L.divIcon({
     html: svg,
     className: '',
     iconSize: [48, 64],
     iconAnchor: [24, 62],
   })
 }
</script>
