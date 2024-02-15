    @http.route('/crear-ticket/', type="json", auth='none', method=['POST'], cors="*", csrf=False)
    def _nuevo_ticket(self, **kw):
        try:
            data = request.jsonrequest
            print(data)
            fecha = datetime.datetime.now()
            contrato = int(data['contrato'])
            partner_id = int(data['partner_id'])
            name = data['name']
            email = data['email']
            description = data['comentario']
            categoria_ticket = int(data['categoria_ticket'])

            conn = psycopg2.connect(
                host=config['gserp_db_host'],
                database=config['gserp_db_name'],
                user=config['gserp_db_user'],
                password=config['gserp_db_password'])

            cursor = conn.cursor(cursor_factory=RealDictCursor)
            query = f"""select c.name from analytic_sale_order_line l, product_product p, product_template t, codigo_servicio c 
                    where l.subscription_product_line_id={contrato} and l.product_id=p.id and p.product_tmpl_id=t.id and 
                    t.tipo_servicio='principal' and l.codigo_servicio=c.id limit 1;"""
            cursor.execute(query)
            cuenta = cursor.fetchall()
            print("Cuenta", cuenta)
            query = f"""select number_next from ir_sequence where code='website.support.ticket';"""
            cursor.execute(query)
            secuencia = cursor.fetchall()
            print("Secuencia", secuencia)
            cuenta = cuenta[0]['name']
            categoria_ticket = http.request.env['botpress_comunication.ticket_categoria_ref'].sudo().search(
                [('id', '=', categoria_ticket)], limit=1)
            query = f"""select s.id sla, r.id sla_rule from website_support_sla_rule r, website_support_sla s 
                where s.name='{categoria_ticket.prioridad}' and r.name='{categoria_ticket.prioridad}' limit 1;"""
            cursor.execute(query)
            sla = cursor.fetchall()
            _logger.info("SLA obtenido: %s", sla)
            print("SLA", sla)
            conn2 = psycopg2.connect(
                host=config['db_host_matrix'],
                database=config['db_name_matrix'],
                user=config['db_user_matrix'],
                password=config['db_password_matrix'])
            cursor2 = conn2.cursor(cursor_factory=RealDictCursor)

            query = f"""select concat(mazs.name, ' ', rcs.name) zona, macs.direccion as direccion, mazs.nombre_zona_servicio
                from matrix_admin_zona_servicio mazs, matrix_admin_codigo_servicio macs
                join res_country_state rcs on macs.provincia = rcs.id
                where mazs.id = macs.zona_servicio_id and macs.name ='{cuenta}'
                and macs.name not like 'V%%' and macs.name not like 'I%%' and macs.name not like 'L%%'
                and macs.name not like 'T%%' and macs.name not like 'X%%' limit 1;"""

            cursor2.execute(query)
            direccion = cursor2.fetchall()
            _logger.info("Dirección obtenida: %s", direccion)
            print("direccion", direccion)
            cursor2.close()
            conn2.close()

            subject = 'CORRECTIVO' if categoria_ticket.identificador_categoria == 8 else (
                'QUEJAS' if categoria_ticket.identificador_categoria == 5 else 'REQUERIMIENTO')
            query = f"""insert into website_support_ticket (ticket_number,channel,partner_id,person_name,category,sub_category_id,email,description,subject,cod_service,cod_service_address,
                                priority_id,sla_timer,sla_id,sla_rule_id,subservice_id,zona,state,create_date,statebar,unattended) values ({secuencia[0]['number_next']},'GS BOT',{partner_id},'{name}',
                                {categoria_ticket.identificador_categoria},{categoria_ticket.identificador_subcategoria},'{email}','{description}',
                                '{subject}','{cuenta}','{direccion[0]['direccion']}',{categoria_ticket.priority},{categoria_ticket.sla_time},{sla[0]['sla']},{sla[0]['sla_rule']},
                                {categoria_ticket.identificador_descripcion if categoria_ticket.identificador_descripcion != 0 else 'null'},'{direccion[0]['zona']}',9,'{fecha}','por_atender',true)"""
            ticket_coincidente = cursor.fetchall()

            _logger.info("Ticket creado: %s", ticket_coincidente)
            print("ticket_coincidente", ticket_coincidente)
            if len(ticket_coincidente) > 0:
                res = {"ticket_creado": True, "ticket_id": ticket_coincidente[0]['id']}
            else:   # Ejecuta el insert
                cursor.execute(query)
                query = f"""update ir_sequence set number_next={secuencia[0]['number_next'] + 1} where code='website.support.ticket';"""
                cursor.execute(query)
                conn.commit()
            cursor.close()
            conn.close()
            return {'status': 200, 'status_response': "ok", 'ticket': secuencia[0]['number_next']}
        except Exception as e:
            _logger.info("Error en la creacion de ticket " + str(e))
            return {'status': 500, 'error': str(e)}
