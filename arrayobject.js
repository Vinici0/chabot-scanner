const cambio_trabajos_equipos_adicionales = [
  {
    id: 1,
    name: "Cambio del Plan",
    categoriaTiket: 56,
  },
  {
    id: 2,
    name: "Mantenimiento Preventivo",
    categoriaTiket: 58,
  },
  {
    id: 3,
    name: "Desmonte de Equipos",
    categoriaTiket: 48,
  },
  {
    id: 4,
    name: "Traslado Equipos",
    categoriaTiket: 55,
  },
  {
    id: 5,
    name: "Equipos Adicionales",
    categoriaTiket: 42,
  },
  {
    id: 6,
    name: "Descarga de video",
    categoriaTiket: 49,
  },
  {
    id: 7,
    name: "Reemplazo de equipos",
    categoriaTiket: 61,
  },
  {
    id: 8,
    name: "Servicio de vigilancia",
    categoriaTiket: 43,
  },
  {
    id: 9,
    name: "Otros",
  },
];

const  Sugerencias_No_Suspensiones = [
  {
    id: 1,
    name: "Sugerencias",
    categoriaTiket: 'pendiente',
  },
  {
    id: 2,
    name: "No Suspensiones",
    categoriaTiket: 59,
  },
  {
    id: 3,
    name: "A",
    categoriaTiket: 54,
  },
  {
    id: 4,
    name: "B",
    categoriaTiket: 41,
  }
  
]

const newCrearTicketST = () => {
  const dataTicket = getObjectTicket()
  const dataSubTicket = 2
  const ticketId = dataTicket.find(item => item.id === dataSubTicket)
  const ticketIdTwo = ticketId.categoriaTiket
  return ticketIdTwo
}

const getObjectTicket = () => {
  const tipoTicketSoporteTecnico = 1
  const optionsTicket = {
    1: [
      {
        id: 1,
        name: 'Sistema Apagado',
        categoriaTiket: 9
      },
      {
        id: 2,
        name: 'Cambio de Claves',
        categoriaTiket: 27
      },
      {
        id: 3,
        name: 'No Armar/Desarmar',
        categoriaTiket: 26
      },
      {
        id: 4,
        name: 'Equipo Averiado',
        categoriaTiket: 26
      },
      {
        id: 5,
        name: 'Otros',
        categoriaTiket: 21
      }
    ],
    //GPS
    2: [
      { id: 1, name: 'Ubicación incorrecta', categoriaTiket: 19 },
      { id: 2, name: 'Equipo averiado', categoriaTiket: 18 },
      { id: 3, name: 'Problemas la APP', categoriaTiket: 38 },
      { id: 4, name: 'Problema con la APP', categoriaTiket: 38 },
      { id: 5, name: 'Otros', categoriaTiket: 38 }
    ],
    //Control de acceso
    3: [
      { id: 1, name: 'Equipos Apagados', categoriaTiket: 12 },
      { id: 2, name: 'Error de autenticación', categoriaTiket: 32 },
      { id: 3, name: 'Otros problemas', categoriaTiket: 23 }
    ],
    //CCTV
    4: [
      { id: 1, name: 'Grabador Apagado', categoriaTiket: 12 },
      { id: 2, name: 'Camara no funciona', categoriaTiket: 30 },
      { id: 3, name: 'No puedo acceder a las grabaciones', categoriaTiket: 31 },
      { id: 4, name: 'Problema con APP', categoriaTiket: 13 },
      { id: 5, name: 'Otros', categoriaTiket: 23 }
    ],
    //Correo electronico
    5: [
      { id: 1, name: 'Electrificador Apagado', categoriaTiket: 14 },
      { id: 2, name: 'Líneas de cerco con problemas', categoriaTiket: 34 },
      { id: 3, name: 'Otros', categoriaTiket: 24 }
    ]
  }

  return optionsTicket[tipoTicketSoporteTecnico]
}


console.log(newCrearTicketST())
