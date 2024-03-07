# chabot-scanner


## Obtener Controto
```
  const obtenerContrato = async () => {
    if (temp.agencia && session.contratos[temp.agencia]) {
      bp.logger.info(
        `RESPONSE ${session.contratos[temp.agencia]['contrato']}, ${JSON.stringify(
          session.contratos[temp.agencia]['contrato']
        )}`
      )

      //Veficica que sea mas de uno
      if (session.contratos[temp.agencia]['contrato'].length > 1) {
        let opciones = []
        session.contratos[temp.agencia]['contrato'].forEach(ser => {
          opciones.push({ title: ser.name, value: ser.id + '' })
        })
        const messageselect = {
          type: 'single-choice', 
          skill: 'choice',
          text: `Seleccione el contrato del que requiere su factura:`,
          dropdownPlaceholder: 'Seleccione...',
          choices: opciones,
          markdown: true
        }
        await bp.events.replyToEvent(event, [messageselect])
        temp.tieneCon = 'true'
      } else {
        //En caso que sea igual a 1 solo retorna la primera posicion
        temp.tieneCon = 'false'
        temp.contrato = session.contratos[temp.agencia]['contrato'][0].id
      }
      temp.selectError = 'false'
    } else {
      temp.selectError = 'true'
    }
  }

  return obtenerContrato()

```


## Parte dos 
```
  const axios = require('axios')
  const obtenerContratos = async value => {
    if (!session.agenciascontratos || (session.agenciascontratos && session.agenciascontratos.length == 0)) {
      const { data } = await axios({
        headers: { 'Content-Type': 'application/json' },
        method: 'get',
        // url: 'https://www.gruposcanner.com/get-sucursales/ref/',
        url: 'http://192.168.15.230:8070/get-contratos/',
        data: {
          ref: value
        }
      })
      bp.logger.info(`RESPONSE ${data}, ${JSON.stringify(data)}`)
      if (data.result && data.result.agencias) {
        session.detallecontratos = data.result.contrato //  value = 1
        session.agenciascontratos = data.result.agencias // value = 1
        //TODO: Borrar logger de prueba
        bp.logger.info(`RESPONSE detallecontratos ${session.detallecontratos}`)
      }
    }
    if (session.agenciascontratos.length > 0) {
      //TODO: En caso solo tenga una agencia
      if (session.agenciascontratos.length == 1) {
        temp.tieneAg = 'false'
        temp.agencia = session.agenciascontratos[0].id + ''
      } else if (session.agenciascontratos.length > 10) {
        //TODO: En caso tenga mas de 10 agencias
        const num_lista =
          session.agenciascontratos.length % 9 == 0
            ? session.agenciascontratos.length / 9
            : Math.trunc(session.agenciascontratos.length / 9) + 1
        for (let i = 0; i < num_lista; i++) {
          let opciones = []
          for (let j = i * 9; j < (i + 1) * 9 && j < session.agenciascontratos.length; j++) {
            opciones.push({ title: session.agenciascontratos[j].name, value: session.agenciascontratos[j].id + '' })
          }
          if (i + 1 < num_lista) {
            opciones.push({ title: 'Otras agencias...', value: 'otras_agencias' })
          }
          const messageselect = {
            type: 'single-choice',
            skill: 'choice',
            text: `Seleccione la agencia de la que desea ver su contrato:`,
            dropdownPlaceholder: 'Selecciona...',
            choices: opciones,
            markdown: true
          }
          bp.logger.info(`RESPONSE ${opciones}, ${JSON.stringify(opciones)}`)
          if (!temp.listasAgencias) {
            temp.listasAgencias = []
          }
          temp.listasAgencias.push(messageselect)
          //await bp.events.replyToEvent(event, [messageselect])
        }

        await bp.events.replyToEvent(event, [temp.listasAgencias[0]])
        temp.numLista = 0
        temp.tieneAg = 'true'
      } else {
        //TODO: En caso tenga de 2 hasta 10 agencias
        let opciones = []
        session.agenciascontratos.forEach(suc => {
          opciones.push({ title: suc.name, value: suc.id + '' })
        })
        const messageselect = {
          type: 'single-choice',
          skill: 'choice',
          text: `Seleccione la agencia de la que desea ver su contrato:`,
          dropdownPlaceholder: 'Selecciona...',
          choices: opciones,
          markdown: true
        }
        await bp.events.replyToEvent(event, [messageselect])
        temp.tieneAg = 'true'
      }
      temp.existeContrato = 'true'
    } else {
      temp.existeContrato = ' false '
    }
  } 
```
