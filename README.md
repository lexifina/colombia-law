# Colombia: law history in git

The law of Colombia as a git history: one file per provision, one commit per law or ruling on the day it took effect, and the act or ruling that made each change as the commit's author. `git blame` names the Acto Legislativo or the Constitutional Court ruling behind every paragraph; `git log` lists every change to an article; checking out a date gives the text in force that day.

It follows the shared design of [lexifina/global-law](https://github.com/lexifina/global-law), which places it at `co/`.

**What is in it now**

| Folder | Act | History |
| --- | --- | --- |
| `constitucion/` | Constitución Política de Colombia (1991) | From promulgation (4 July 1991) to today: every Acto Legislativo that amended it, the 1991 Aclaración of Gaceta Constitucional No. 125, and the Constitutional Court rulings that struck amendments or parts of them |
| `codigo-civil/` | Código Civil (Ley 84 de 1873) | From its sanction (26 May 1873), in the 1873 text the source reproduces, to today |
| `ley-1581-2012/` | Ley 1581 de 2012 (protección de datos personales) | From promulgation (18 October 2012) to today |
| `codigo-penal/` | Código Penal (Ley 599 de 2000) | From its entry into force (24 July 2001, one year after promulgation, art. 476) to today |
| `codigo-general-del-proceso/` | Código General del Proceso (Ley 1564 de 2012) | From promulgation (12 July 2012; art. 627 staggers the start of most articles, see the first commit) to today |
| `codigo-sustantivo-del-trabajo/` | Código Sustantivo del Trabajo | From the official edition (Diario Oficial No. 27.622, 7 June 1951; Decretos 2663 and 3743 de 1950) to today |
| `codigo-de-comercio/` | Código de Comercio (Decreto 410 de 1971) | From its issue (27 March 1971; most of it from 1 January 1972, art. 2038) to today |
| `cpaca/` | Código de Procedimiento Administrativo y de lo Contencioso Administrativo (Ley 1437 de 2011) | From its entry into force (2 July 2012, art. 308) to today |
| `codigo-de-procedimiento-penal/` | Código de Procedimiento Penal (Ley 906 de 2004) | From publication (1 September 2004; by judicial district from 2005, art. 530) to today; one change on `futuro` |
| `codigo-de-la-infancia-y-la-adolescencia/` | Código de la Infancia y la Adolescencia (Ley 1098 de 2006) | From promulgation (8 November 2006; most of it six months later, art. 216) to today |
| `codigo-nacional-de-seguridad-y-convivencia-ciudadana/` | Código Nacional de Seguridad y Convivencia Ciudadana (Ley 1801 de 2016) | From its entry into force (29 January 2017, six months after promulgation, art. 243) to today |
| `sistema-de-seguridad-social-integral/` | Ley 100 de 1993 (Sistema de Seguridad Social Integral) | From publication (23 December 1993, art. 289; pensions from 1 April 1994, art. 151) to today |
| `codigo-general-disciplinario/` | Código General Disciplinario (Ley 1952 de 2019) | From promulgation (28 January 2019; in force only from 29 March 2022, see the first commit) to today |
| `codigo-electoral/` | Código Electoral (Decreto 2241 de 1986) | From publication (1 August 1986, art. 218) to today |
| `estatuto-tributario/` | Estatuto Tributario (Decreto 624 de 1989) | From its entry into force (30 May 1989, two months after publication, the decree's art. 3) to today, including the yearly decrees that updated its absolute values before the UVT |
| `estatuto-general-de-contratacion/` | Estatuto General de Contratación de la Administración Pública (Ley 80 de 1993) | From promulgation (28 October 1993; most of it from 1 January 1994, art. 81) to today |
| `estatuto-del-consumidor/` | Estatuto del Consumidor (Ley 1480 de 2011) | From its entry into force (12 April 2012, six months after promulgation, art. 84) to today |
| `codigo-nacional-de-transito/` | Código Nacional de Tránsito Terrestre (Ley 769 de 2002) | From its entry into force (13 December 2002, three months after promulgation, art. 170) to today |
| `estatuto-organico-del-sistema-financiero/` | Estatuto Orgánico del Sistema Financiero (Decreto 663 de 1993) | From its entry into force (2 May 1993, art. 339) to today |
| `codigo-de-minas/` | Código de Minas (Ley 685 de 2001) | From promulgation (8 September 2001, art. 362) to today, including the reform of Ley 1382 de 2010 until Sentencia C-366 de 2011's deferred effect ended (13 May 2013) |
| `codigo-procesal-del-trabajo-1948/` | Código Procesal del Trabajo y de la Seguridad Social (Decreto-Ley 2158 de 1948) | From its entry into force (29 June 1948, five days after issue, art. 156) to its repeal as a whole by Ley 2452 de 2025 (2 April 2026); the folder is empty from that day |
| `codigo-procesal-del-trabajo/` | Código Procesal del Trabajo y de la Seguridad Social (Ley 2452 de 2025) | From its entry into force (2 April 2026, one year after publication, art. 330) to today |
| `regimen-de-insolvencia/` | Régimen de Insolvencia Empresarial (Ley 1116 de 2006) | From promulgation (27 December 2006; most of it six months later, art. 126) to today |
| `servicios-publicos-domiciliarios/` | Régimen de los Servicios Públicos Domiciliarios (Ley 142 de 1994) | From publication (11 July 1994, art. 189) to today |
| `ley-1150-2007/` | Ley 1150 de 2007 (eficiencia y transparencia en la contratación pública) | From promulgation (16 July 2007; most of it six months later, art. 33) to today |
| `estatuto-anticorrupcion/` | Estatuto Anticorrupción (Ley 1474 de 2011) | From promulgation (12 July 2011, art. 135) to today, including the articles the Código General Disciplinario repealed from 29 March 2022 |
| `ley-de-transparencia/` | Ley de Transparencia y del Derecho de Acceso a la Información Pública Nacional (Ley 1712 de 2014) | From its entry into force for national bodies (6 September 2014, six months after promulgation; territorial bodies a year after, art. 33) to today |
| `ley-789-2002/` | Ley 789 de 2002 (protección social y reforma laboral) | From publication (27 December 2002, art. 52) to today |
| `ley-de-formalizacion-y-generacion-de-empleo/` | Ley de Formalización y Generación de Empleo (Ley 1429 de 2010) | From publication (29 December 2010, art. 65) to today |
| `gestion-del-riesgo-de-desastres/` | Política Nacional de Gestión del Riesgo de Desastres (Ley 1523 de 2012) | From publication (24 April 2012, art. 96) to today |
| `ley-general-ambiental/` | Ley General Ambiental (Ley 99 de 1993) | From promulgation (22 December 1993, art. 118) to today, including the emergency decrees of 1999, 2000, 2011 and 2023 until the rulings that struck them |
| `ley-de-desarrollo-territorial/` | Ley de Desarrollo Territorial (Ley 388 de 1997) | From publication (24 July 1997, art. 138) to today |
| `codigo-de-recursos-naturales/` | Código Nacional de Recursos Naturales Renovables y de Protección al Medio Ambiente (Decreto Ley 2811 de 1974) | From its issue (18 December 1974, art. 340) to today |
| `ley-estatutaria-de-la-administracion-de-justicia/` | Ley Estatutaria de la Administración de Justicia (Ley 270 de 1996) | From promulgation (15 March 1996, art. 210) to today |
| `codigo-disciplinario-unico/` | Código Disciplinario Único (Ley 734 de 2002) | From its entry into force (5 May 2002, three months after sanction, art. 224) to its repeal by the Código General Disciplinario on 29 March 2022 (its art. 30 until 29 December 2023) |
| `codigo-penitenciario-y-carcelario/` | Código Penitenciario y Carcelario (Ley 65 de 1993) | From promulgation (20 August 1993, art. 174) to today |
| `ley-de-victimas-y-restitucion-de-tierras/` | Ley de Víctimas y Restitución de Tierras (Ley 1448 de 2011) | From promulgation (10 June 2011, art. 208) to today |
| `ley-general-de-educacion/` | Ley General de Educación (Ley 115 de 1994) | From promulgation (8 February 1994, art. 222) to today |
| `educacion-superior/` | Servicio Público de la Educación Superior (Ley 30 de 1992) | From promulgation (29 December 1992, art. 144) to today |
| `regimen-municipal/` | Régimen Municipal (Ley 136 de 1994) | From publication (2 June 1994, art. 203) to today |
| `sociedad-por-acciones-simplificada/` | Sociedad por Acciones Simplificada (Ley 1258 de 2008) | From promulgation (5 December 2008, art. 46) to today |
| `habeas-data/` | Ley de Hábeas Data (Ley 1266 de 2008) | From publication (31 December 2008, art. 22) to today |
| `comercio-electronico/` | Ley de Comercio Electrónico (Ley 527 de 1999) | From publication (21 August 1999, art. 47) to today |
| `reglamento-del-congreso/` | Reglamento del Congreso (Ley 5 de 1992) | From promulgation (18 June 1992, art. 393) to today |
| `accion-de-tutela/` | Acción de tutela (Decreto 2591 de 1991) | From publication (19 November 1991, art. 55) to today |
| `acciones-populares-y-de-grupo/` | Acciones populares y de grupo (Ley 472 de 1998) | From its entry into force (6 August 1999, one year after promulgation, art. 86) to today |
| `accion-de-cumplimiento/` | Acción de cumplimiento (Ley 393 de 1997) | From publication (30 July 1997, art. 32) to today |
| `codigo-disciplinario-del-abogado/` | Código Disciplinario del Abogado (Ley 1123 de 2007) | From its entry into force (22 May 2007, four months after promulgation, art. 112) to today |
| `codigo-de-extincion-de-dominio/` | Código de Extinción de Dominio (Ley 1708 de 2014) | From its entry into force (20 July 2014, six months after promulgation, art. 218) to today |
| `estatuto-de-arbitraje/` | Estatuto de Arbitraje Nacional e Internacional (Ley 1563 de 2012) | From its entry into force (12 October 2012, three months after promulgation, art. 119) to today |
| `estatuto-de-conciliacion/` | Estatuto de Conciliación (Ley 2220 de 2022) | From its entry into force (30 December 2022, six months after promulgation, art. 145) to today |
| `codigo-de-procedimiento-penal-2000/` | Código de Procedimiento Penal de 2000 (Ley 600 de 2000) | From its entry into force (24 July 2001, one year after promulgation, art. 536) to today; for crimes after 1 January 2005 the Código de Procedimiento Penal of 2004 applies, as the source notes on each article |
| `responsabilidad-fiscal/` | Responsabilidad fiscal (Ley 610 de 2000) | From publication (18 August 2000, art. 69) to today |
| `mecanismos-de-participacion-ciudadana/` | Mecanismos de participación ciudadana (Ley 134 de 1994) | From publication (31 May 1994, art. 109) to today |
| `organizacion-de-la-administracion-publica/` | Organización y funcionamiento de la administración pública (Ley 489 de 1998) | From promulgation (30 December 1998, art. 121) to today |
| `empleo-publico-y-carrera-administrativa/` | Empleo público y carrera administrativa (Ley 909 de 2004) | From publication (23 September 2004, art. 58) to today |
| `ley-organica-del-plan-de-desarrollo/` | Ley Orgánica del Plan de Desarrollo (Ley 152 de 1994) | From promulgation (19 July 1994, art. 52) to today |
| `ley-organica-de-ordenamiento-territorial/` | Ley Orgánica de Ordenamiento Territorial (Ley 1454 de 2011) | From promulgation (29 June 2011, art. 40) to today |
| `ley-617-2000/` | Ley 617 de 2000 (categorías y gasto de las entidades territoriales) | From promulgation (9 October 2000, art. 96) to today |
| `sistema-general-de-participaciones/` | Sistema General de Participaciones (Ley 715 de 2001) | From its sanction (21 December 2001, art. 113) to today |
| `control-fiscal/` | Control fiscal (Ley 42 de 1993) | From promulgation (27 January 1993, art. 110) to today, including the 26 articles Decreto Ley 403 de 2020 repealed until the rulings of 2022 and 2023 revived them |
| `participacion-democratica/` | Participación democrática (Ley 1757 de 2015) | From promulgation (6 July 2015, art. 113) to today |
| `estatuto-organico-del-presupuesto/` | Estatuto Orgánico del Presupuesto (Decreto 111 de 1996) | From publication (18 January 1996, the decree's art. 2) to today; two changes on `futuro` (1 January 2027, Sentencia C-116 de 2026) |
| `estatuto-organico-de-bogota/` | Estatuto Orgánico de Bogotá (Decreto 1421 de 1993) | From publication (22 July 1993, art. 180) to today |
| `proteccion-de-la-competencia/` | Protección de la competencia (Ley 1340 de 2009) | From publication (24 July 2009, art. 34) to today |
| `competencia-desleal/` | Competencia desleal (Ley 256 de 1996) | From promulgation (18 January 1996, art. 33) to today |
| `tecnologias-de-la-informacion-y-las-comunicaciones/` | Tecnologías de la Información y las Comunicaciones (Ley 1341 de 2009) | From promulgation (30 July 2009; some articles six months later, art. 73) to today |
| `ley-estatutaria-de-salud/` | Ley Estatutaria de Salud (Ley 1751 de 2015) | From publication (16 February 2015, art. 26) to today |
| `reforma-del-sistema-de-salud-2011/` | Reforma del Sistema General de Seguridad Social en Salud (Ley 1438 de 2011) | From publication (19 January 2011, art. 145) to today |
| `violencia-contra-las-mujeres/` | Violencia y discriminación contra las mujeres (Ley 1257 de 2008) | From promulgation (4 December 2008, art. 39) to today |
| `acoso-laboral/` | Acoso laboral (Ley 1010 de 2006) | From promulgation (23 January 2006, art. 19) to today |
| `riesgos-laborales/` | Sistema de Riesgos Laborales (Ley 1562 de 2012) | From publication (11 July 2012, art. 33) to today |
| `garantias-mobiliarias/` | Garantías mobiliarias (Ley 1676 de 2013) | From its entry into force (20 February 2014, six months after promulgation, art. 91) to today |
| `reforma-agraria/` | Sistema Nacional de Reforma Agraria y Desarrollo Rural Campesino (Ley 160 de 1994) | From promulgation (5 August 1994, art. 112) to today |
| `asociaciones-publico-privadas/` | Asociaciones Público Privadas (Ley 1508 de 2012) | From 10 March 2012 (it gives no day of its own: two months after promulgation, Ley 4 de 1913, art. 52) to today |
| `infraestructura-de-transporte/` | Infraestructura de transporte (Ley 1682 de 2013) | From its first publication (22 November 2013, art. 73) to today |
| `soborno-transnacional/` | Responsabilidad de las personas jurídicas por soborno transnacional (Ley 1778 de 2016) | From promulgation (2 February 2016, art. 37) to today |
| `procedimiento-sancionatorio-ambiental/` | Procedimiento sancionatorio ambiental (Ley 1333 de 2009) | From promulgation (21 July 2009, art. 66) to today |
| `ley-general-de-cultura/` | Ley General de Cultura (Ley 397 de 1997) | From its sanction (7 August 1997, art. 83) to today |
| `ley-del-deporte/` | Ley del Deporte (Ley 181 de 1995) | From promulgation (18 January 1995, art. 91) to today |
| `ley-general-de-turismo/` | Ley General de Turismo (Ley 300 de 1996) | From publication (30 July 1996, art. 113) to today |
| `reforma-del-sistema-de-salud-2007/` | Reforma del Sistema General de Seguridad Social en Salud (Ley 1122 de 2007) | From publication (9 January 2007, art. 46) to today |
| `derechos-de-las-personas-con-discapacidad/` | Derechos de las personas con discapacidad (Ley 1618 de 2013) | From publication (27 February 2013, art. 32) to today |
| `capacidad-legal-de-las-personas-con-discapacidad/` | Capacidad legal de las personas con discapacidad (Ley 1996 de 2019) | From promulgation (26 August 2019, art. 63; some parts later, art. 52) to today |
| `violencia-intrafamiliar/` | Violencia intrafamiliar (Ley 294 de 1996) | From promulgation (22 July 1996, art. 31) to today |
| `violencia-sexual-contra-ninos/` | Prevención de la violencia sexual contra niños, niñas y adolescentes (Ley 1146 de 2007) | From publication (10 July 2007, art. 19) to today |
| `adultos-mayores/` | Derechos de los adultos mayores (Ley 1251 de 2008) | From promulgation (27 November 2008, art. 35) to today |
| `proteccion-integral-a-la-familia/` | Ley de Protección Integral a la Familia (Ley 1361 de 2009) | From publication (3 December 2009, art. 14) to today |
| `estatuto-de-ciudadania-juvenil/` | Estatuto de Ciudadanía Juvenil (Ley 1622 de 2013) | From promulgation (29 April 2013, art. 79) to today |
| `tic-en-las-actuaciones-judiciales/` | Tecnologías de la información en las actuaciones judiciales (Ley 2213 de 2022) | From promulgation (13 June 2022, art. 15) to today |
| `cartera-publica/` | Normalización de la cartera pública (Ley 1066 de 2006) | From promulgation (29 July 2006, art. 21) to today |
| `modernizacion-de-los-municipios/` | Modernización de la organización y el funcionamiento de los municipios (Ley 1551 de 2012) | From publication (6 July 2012, art. 50) to today |
| `areas-metropolitanas/` | Régimen de las Áreas Metropolitanas (Ley 1625 de 2013) | From publication (29 April 2013, art. 42) to today |
| `regimen-departamental/` | Régimen Departamental (Ley 2200 de 2022) | From publication (8 February 2022, art. 154) to today |
| `propiedad-horizontal/` | Régimen de Propiedad Horizontal (Ley 675 de 2001) | From publication (4 August 2001, art. 87) to today |
| `arrendamiento-de-vivienda-urbana/` | Arrendamiento de vivienda urbana (Ley 820 de 2003) | From promulgation (10 July 2003, art. 43) to today |
| `estatuto-de-registro-de-instrumentos-publicos/` | Estatuto de Registro de Instrumentos Públicos (Ley 1579 de 2012) | From promulgation (1 October 2012, art. 104) to today |
| `financiacion-de-vivienda/` | Financiación de vivienda (Ley 546 de 1999) | From promulgation (23 December 1999, art. 58) to today |
| `desarrollo-urbano-y-vivienda/` | Desarrollo urbano y acceso a la vivienda (Ley 1537 de 2012) | From promulgation (20 June 2012, art. 66) to today |
| `ley-electrica/` | Ley Eléctrica (Ley 143 de 1994) | From promulgation (12 July 1994, art. 97) to today |
| `energias-renovables/` | Energías renovables no convencionales (Ley 1715 de 2014) | From promulgation (13 May 2014, art. 46) to today |
| `cambio-climatico/` | Gestión del cambio climático (Ley 1931 de 2018) | From promulgation (27 July 2018, art. 36) to today |
| `personas-con-discapacidad-mental/` | Protección de personas con discapacidad mental (Ley 1306 de 2009) | From promulgation (5 June 2009, art. 120) to today; most of its articles repealed by Ley 1996 de 2019 (26 August 2019) |
| `ley-de-transporte/` | Ley de Transporte (Ley 105 de 1993) | From publication (30 December 1993, art. 71) to today |
| `estatuto-nacional-de-transporte/` | Estatuto Nacional de Transporte (Ley 336 de 1996) | From promulgation (28 December 1996, art. 90) to today |
| `codigo-sanitario-nacional/` | Código Sanitario Nacional (Ley 9 de 1979) | From its sanction (24 January 1979, art. 607) to today |
| `codigo-de-regimen-municipal/` | Código de Régimen Municipal (Decreto 1333 de 1986) | From publication (14 May 1986, art. 386) to today |
| `estatuto-basico-de-los-partidos/` | Estatuto Básico de los partidos y movimientos políticos (Ley 130 de 1994) | From publication (23 March 1994, art. 54) to today |
| `partidos-y-procesos-electorales/` | Organización de los partidos y movimientos políticos y de los procesos electorales (Ley 1475 de 2011) | From promulgation (14 July 2011, art. 55) to today |
| `ley-de-garantias-electorales/` | Ley de Garantías Electorales (Ley 996 de 2005) | From promulgation (24 November 2005, art. 42) to today |
| `disposiciones-electorales-1994/` | Disposiciones en materia electoral (Ley 163 de 1994) | From promulgation (2 September 1994, art. 18) to today |
| `estatuto-de-la-oposicion/` | Estatuto de la Oposición Política (Ley 1909 de 2018) | From 20 July 2018 (art. 32) to today |
| `veedurias-ciudadanas/` | Veedurías ciudadanas (Ley 850 de 2003) | From promulgation (19 November 2003, art. 24) to today |
| `mipymes/` | Micro, pequeñas y medianas empresas (Ley 590 de 2000) | From promulgation (12 July 2000, art. 47) to today |
| `ley-de-emprendimiento/` | Ley de Emprendimiento (Ley 2069 de 2020) | From promulgation (31 December 2020, art. 84) to today |
| `cultura-del-emprendimiento/` | Fomento a la cultura del emprendimiento (Ley 1014 de 2006) | From promulgation (27 January 2006, art. 24) to today |
| `regimen-salarial-y-prestacional/` | Régimen salarial y prestacional de los empleados públicos (Ley 4 de 1992) | From promulgation (18 May 1992, art. 22) to today |
| `sistema-general-de-regalias/` | Sistema General de Regalías (Ley 2056 de 2020) | From 1 January 2021 (art. 211) to today |
| `integracion-social-de-personas-con-limitacion/` | Integración social de las personas con limitación (Ley 361 de 1997) | From publication (11 February 1997, art. 73) to today |
| `teletrabajo/` | Teletrabajo (Ley 1221 de 2008) | From publication (16 July 2008, art. 9) to today |
| `trabajo-en-casa/` | Trabajo en casa (Ley 2088 de 2021) | From promulgation (12 May 2021, art. 16) to today |
| `trabajo-remoto/` | Trabajo remoto (Ley 2121 de 2021) | From promulgation (3 August 2021, art. 27) to today |
| `salud-mental/` | Ley de Salud Mental (Ley 1616 de 2013) | From publication (21 January 2013, art. 44) to today |
| `transparencia-y-lucha-contra-la-corrupcion/` | Transparencia, prevención y lucha contra la corrupción (Ley 2195 de 2022) | From promulgation (18 January 2022, art. 69) to today |
| `racionalizacion-de-tramites/` | Racionalización de trámites (Ley 2052 de 2020) | From promulgation (25 August 2020, art. 31) to today |
| `sanciones-por-corrupcion/` | Sanciones para condenados por corrupción (Ley 2014 de 2019) | From promulgation (30 December 2019, art. 10) to today |
| `sistema-nacional-de-discapacidad/` | Sistema Nacional de Discapacidad (Ley 1145 de 2007) | From promulgation (10 July 2007, art. 19) to today |
| `reforma-financiera-2009/` | Reforma financiera y régimen de protección al consumidor financiero (Ley 1328 de 2009) | From promulgation (15 July 2009; arts. 1 to 22 from 1 July 2010, art. 101) to today |
| `mercado-de-valores/` | Ley del Mercado de Valores (Ley 964 de 2005) | From promulgation (8 July 2005; some parts later, art. 86) to today |
| `reforma-pensional-2003/` | Reforma del sistema general de pensiones (Ley 797 de 2003) | From publication (29 January 2003, art. 24) to today |
| `factura-como-titulo-valor/` | Factura como título valor (Ley 1231 de 2008) | From its entry into force (17 October 2008, three months after promulgation, art. 10) to today |
| `servicios-financieros-transaccionales/` | Servicios financieros transaccionales (Ley 1735 de 2014) | From promulgation (21 October 2014, art. 15) to today |
| `conglomerados-financieros/` | Conglomerados financieros (Ley 1870 de 2017) | From promulgation (21 September 2017; Título I later, art. 12) to today |
| `sistema-financiero-y-asegurador-1999/` | Sistema financiero y asegurador (Ley 510 de 1999) | From publication (4 August 1999, art. 123) to today |
| `desarrollo-agropecuario-y-pesquero/` | Ley General de Desarrollo Agropecuario y Pesquero (Ley 101 de 1993) | From promulgation (23 December 1993, art. 100) to today |
| `zidres/` | Zonas de Interés de Desarrollo Rural, Económico y Social (Ley 1776 de 2016) | From promulgation (29 January 2016, art. 32) to today |
| `codigo-penal-militar/` | Código Penal Militar (Ley 1407 de 2010) | From publication (17 August 2010, art. 628) to today |
| `codigo-disciplinario-militar/` | Código Disciplinario Militar (Ley 1862 de 2017) | From its entry into force (4 February 2018, six months after sanction, art. 252) to today |
| `regimen-disciplinario-de-la-policia/` | Régimen Disciplinario para la Policía Nacional (Ley 1015 de 2006) | From its entry into force (7 May 2006, three months after sanction, art. 60) to today |
| `habeas-corpus/` | Hábeas corpus (Ley 1095 de 2006) | From promulgation (2 November 2006, art. 10) to today |
| `estados-de-excepcion/` | Estados de Excepción (Ley 137 de 1994) | From promulgation (3 June 1994, art. 59) to today |
| `inteligencia-y-contrainteligencia/` | Inteligencia y contrainteligencia (Ley 1621 de 2013) | From publication (17 April 2013, art. 46) to today |
| `orden-publico/` | Orden público y convivencia (Ley 418 de 1997) | From promulgation (26 December 1997, art. 132) to today, with its extensions |
| `justicia-y-paz/` | Ley de Justicia y Paz (Ley 975 de 2005) | From promulgation (25 July 2005, art. 72) to today |
| `estatutaria-de-la-jep/` | Estatutaria de la Administración de Justicia en la Jurisdicción Especial para la Paz (Ley 1957 de 2019) | From promulgation (6 June 2019, art. 159) to today |
| `procedimiento-de-la-jep/` | Reglas de procedimiento de la Jurisdicción Especial para la Paz (Ley 1922 de 2018) | From promulgation (18 July 2018, art. 76) to today |
| `evaluacion-de-la-calidad-de-la-educacion/` | Evaluación de la calidad de la educación (Ley 1324 de 2009) | From promulgation (13 July 2009, art. 15) to today |
| `registro-calificado/` | Registro calificado de programas de educación superior (Ley 1188 de 2008) | From promulgation (25 April 2008, art. 7) to today |
| `educacion-tecnica-y-tecnologica/` | Educación superior técnica profesional y tecnológica (Ley 749 de 2002) | From promulgation (19 July 2002, art. 20) to today |
| `ciencia-tecnologia-e-innovacion/` | Ciencia, tecnología e innovación (Ley 1286 de 2009) | From promulgation (23 January 2009, art. 35) to today |
| `ministerio-de-ciencia/` | Ministerio de Ciencia, Tecnología e Innovación (Ley 1951 de 2019) | From publication (24 January 2019, art. 5) to today |
| `inspeccion-de-la-educacion-superior/` | Inspección y vigilancia de la educación superior (Ley 1740 de 2014) | From publication (23 December 2014, art. 26) to today |
| `convivencia-escolar/` | Sistema Nacional de Convivencia Escolar (Ley 1620 de 2013) | From publication (15 March 2013, art. 40) to today |
| `educacion-para-el-trabajo/` | Educación para el trabajo y el desarrollo humano (Ley 1064 de 2006) | From promulgation (26 July 2006, art. 9) to today |
| `espectaculos-publicos-de-las-artes-escenicas/` | Espectáculos públicos de las artes escénicas (Ley 1493 de 2011) | From promulgation (26 December 2011, art. 37) to today |
| `economia-creativa/` | Economía creativa, Ley Naranja (Ley 1834 de 2017) | From promulgation (23 May 2017, art. 15) to today |
| `atencion-integral-del-cancer/` | Ley Sandra Ceballos, atención integral del cáncer (Ley 1384 de 2010) | From promulgation (19 April 2010, art. 24) to today |
| `cuidados-paliativos/` | Ley Consuelo Devis Saavedra, cuidados paliativos (Ley 1733 de 2014) | From its sanction (8 September 2014, art. 11) to today |
| `prevencion-del-consumo-de-tabaco/` | Prevención del consumo de tabaco (Ley 1335 de 2009) | From promulgation (21 July 2009, art. 36) to today |
| `consumo-de-sustancias-psicoactivas/` | Atención integral a personas que consumen sustancias psicoactivas (Ley 1566 de 2012) | From promulgation (31 July 2012, art. 12) to today |
| `obesidad/` | Obesidad y enfermedades crónicas no transmisibles (Ley 1355 de 2009) | From promulgation (14 October 2009, art. 22) to today |
| `enfermedades-huerfanas/` | Enfermedades huérfanas (Ley 1392 de 2010) | From publication (2 July 2010, art. 16) to today |
| `enfermedades-ruinosas-o-catastroficas/` | Enfermedades ruinosas o catastróficas, VIH/Sida (Ley 972 de 2005) | From publication (15 July 2005, art. 7) to today |
| `donacion-de-componentes-anatomicos/` | Donación de componentes anatómicos (Ley 1805 de 2016) | From promulgation (4 August 2016, art. 22) to today |
| `talento-humano-en-salud/` | Talento humano en salud (Ley 1164 de 2007) | From promulgation (4 October 2007, art. 39) to today |
| `epilepsia/` | Protección de las personas que padecen epilepsia (Ley 1414 de 2010) | From promulgation (11 November 2010, art. 27) to today |
| `moralidad-en-la-administracion-publica/` | Moralidad en la administración pública y lucha contra la corrupción (Ley 190 de 1995) | From promulgation (6 June 1995, art. 85) to today |
| `control-interno/` | Control interno de las entidades del Estado (Ley 87 de 1993) | From promulgation (29 November 1993, art. 16) to today |
| `amnistia-indulto-y-tratamientos-penales-especiales/` | Amnistía, indulto y tratamientos penales especiales (Ley 1820 de 2016) | From the day after its publication (31 December 2016, art. 61) to today |
| `contabilidad-e-informacion-financiera/` | Principios y normas de contabilidad e información financiera (Ley 1314 de 2009) | From publication (13 July 2009, art. 17) to today |
| `ejercicio-de-la-ingenieria/` | Ejercicio de la ingeniería y Código de Ética Profesional (Ley 842 de 2003) | From publication (14 October 2003, art. 78) to today |
| `proteccion-al-cesante/` | Mecanismo de protección al cesante (Ley 1636 de 2013) | From publication (18 June 2013, art. 49) to today |
| `derecho-de-autor-1993/` | Derecho de autor, reforma de la Ley 23 de 1982 (Ley 44 de 1993) | From publication (5 February 1993, art. 70) to today |
| `construcciones-sismo-resistentes/` | Construcciones sismo resistentes (Ley 400 de 1997) | From six months after its sanction (19 February 1998, art. 56) to today |
| `libranza/` | Libranza o descuento directo (Ley 1527 de 2012) | From promulgation (27 April 2012, art. 23; arts. 6 and 8 six months later) to today |
| `codigo-de-etica-y-disciplinario-del-congresista/` | Código de Ética y Disciplinario del Congresista (Ley 1828 de 2017) | From publication (23 January 2017, art. 73) to today |
| `codigo-contencioso-administrativo-1984/` | Código Contencioso Administrativo (Decreto 1 de 1984) | From its entry into force (1 March 1984, art. 2 of the decree) to its repeal by Ley 1437 de 2011 (2 July 2012; its arts. 5 to 26, on the right of petition, on 1 January 2015); the folder is empty from then |
| `codigo-nacional-de-policia-1970/` | Código Nacional de Policía (Decreto 1355 de 1970) | From its entry into force (4 November 1970, two months after promulgation under the default rule) to its repeal by Ley 1801 de 2016 (29 January 2017); Título IV, added by Decreto 522 de 1971, numbers its articles from 1 (`art-tiv-NNN`); the folder is empty from the repeal |
| `codigo-del-menor/` | Código del Menor (Decreto 2737 de 1989) | From publication (27 November 1989, art. 354) to its repeal by Ley 1098 de 2006 in stages: most articles on 8 May 2007, those on offences by minors on 31 December 2009, those Ley 1098 kept on 1 January 2014 (Código General del Proceso); art. 152, printed with no repeal marker, is still there |
| `codigo-de-procedimiento-civil-1970/` | Código de Procedimiento Civil (Decreto 1400 de 1970) | From its entry into force (1 July 1971, art. 699 as Decreto 1678 de 1970 rewrote it) to its repeal by the Código General del Proceso (Ley 1564 de 2012, art. 626), dated 1 January 2014 as the source dates it (the new code took effect gradually by judicial district); a few articles earlier; the folder is empty from then |
| `codigo-de-regimen-departamental/` | Código de Régimen Departamental (Decreto 1222 de 1986) | From its first publication (14 May 1986, art. 340) to today: the 106 articles Ley 2200 de 2022 repealed leave on 8 February 2022; those on departmental property, contracts and revenue that it kept, and the others the source prints, are still there |
| `ejercicio-de-la-psicologia/` | Ejercicio de la psicología y Código Deontológico y Bioético (Ley 1090 de 2006) | From its entry into force (6 September 2006, art. 93) to today |
| `empleo-y-emprendimiento-juvenil/` | Empleo y emprendimiento juvenil (Ley 1780 de 2016) | From its entry into force (2 May 2016, art. 28) to today |
| `fajas-de-retiro-de-carreteras/` | Fajas de retiro de las carreteras y Sistema Integral Nacional de Información de Carreteras (Ley 1228 de 2008) | From its entry into force (16 July 2008, art. 12) to today |
| `vivienda-segura/` | Protección del comprador de vivienda y seguridad de las edificaciones (Ley 1796 de 2016) | From its entry into force (13 July 2016, art. 36) to today; its Título IV took effect a year later (13 July 2017); arts. 30 and 31 out from 21 June 2020 (Sentencia C-568-19) |
| `vivienda-y-habitat/` | Vivienda y hábitat (Ley 2079 de 2021) | From its entry into force (14 January 2021, art. 59) to today |
| `voto-programatico/` | Voto programático (Ley 131 de 1994) | From its entry into force (9 May 1994, art. 16) to today |
| `trata-de-personas/` | Trata de personas (Ley 985 de 2005) | From its entry into force (29 August 2005, art. 23) to today |
| `comisarias-de-familia/` | Comisarías de Familia (Ley 2126 de 2021) | From its entry into force (4 August 2021, art. 47) to today; the provisions its art. 47 lists took effect two years later |
| `cero-a-siempre/` | Política de Estado para el Desarrollo Integral de la Primera Infancia de Cero a Siempre (Ley 1804 de 2016) | From its entry into force (2 August 2016, art. 28) to today |
| `habitantes-de-la-calle/` | Política pública social para habitantes de la calle (Ley 1641 de 2013) | From its entry into force (12 July 2013, art. 14) to today |
| `comunidades-negras/` | Comunidades negras (Ley 70 de 1993) | From its entry into force (31 August 1993, art. 68) to today |
| `desplazamiento-forzado/` | Desplazamiento forzado (Ley 387 de 1997) | From its entry into force (24 July 1997, art. 34) to today |
| `ley-de-cuotas/` | Participación de la mujer en los niveles decisorios del poder público, ley de cuotas (Ley 581 de 2000) | From its entry into force (31 May 2000, art. 17) to today |
| `igualdad-de-oportunidades-para-las-mujeres/` | Igualdad de oportunidades para las mujeres (Ley 823 de 2003) | From its entry into force (11 July 2003, art. 14) to today |
| `igualdad-salarial/` | Igualdad salarial entre mujeres y hombres (Ley 1496 de 2011) | From its entry into force (29 December 2011, art. 10) to today |
| `economia-del-cuidado/` | Economía del cuidado (Ley 1413 de 2010) | From its entry into force (11 November 2010, art. 8) to today |
| `mujeres-rurales/` | Mujeres rurales (Ley 731 de 2002) | From its entry into force (16 January 2002, art. 35) to today |
| `servicio-nacional-de-aprendizaje/` | Servicio Nacional de Aprendizaje, SENA (Ley 119 de 1994) | From its entry into force (9 February 1994, art. 51) to today |
| `servicios-postales/` | Servicios postales (Ley 1369 de 2009) | From its entry into force (30 December 2009, art. 53) to today |
| `accion-comunal/` | Acción comunal (Ley 2166 de 2021) | From its entry into force (18 December 2021, art. 109) to today |
| `ventas-multinivel/` | Actividades de comercialización en red o mercadeo multinivel (Ley 1700 de 2013) | From its entry into force (27 December 2013, art. 13) to today |
| `distritos-especiales/` | Régimen de los distritos especiales (Ley 1617 de 2013) | From its entry into force (5 February 2013, art. 138) to today |
| `distritos-de-barranquilla-cartagena-y-santa-marta/` | Régimen de los distritos de Barranquilla, Cartagena y Santa Marta (Ley 768 de 2002) | From its entry into force (7 August 2002, art. 49) to today |
| `television/` | Servicio de televisión (Ley 182 de 1995) | From its entry into force (20 January 1995, art. 65) to today |
| `historia-clinica-electronica/` | Historia clínica electrónica interoperable (Ley 2015 de 2020) | From its entry into force (31 January 2020, art. 16) to today |
| `telesalud/` | Telesalud (Ley 1419 de 2010) | From its entry into force (13 December 2010, art. 12) to today |
| `accesibilidad/` | Accesibilidad de las personas con discapacidad, adición a la Ley 361 de 1997 (Ley 1287 de 2009) | From its entry into force (3 March 2009, art. 9) to today |
| `accion-comunal-2002/` | Acción comunal (Ley 743 de 2002) | From its entry into force (7 June 2002, art. 79) to its repeal by Ley 2166 de 2021 (18 December 2021); the folder is empty from then |
| `ley-de-la-juventud/` | Ley de la juventud (Ley 375 de 1997) | From its entry into force (9 July 1997, art. 51) to its repeal by Ley 1622 de 2013 (29 April 2013); the folder is empty from then |
| `control-fiscal-2020/` | Fortalecimiento del control fiscal (Decreto Ley 403 de 2020) | From its entry into force (16 March 2020, art. 166) to today |
| `responsabilidad-fiscal-y-transparencia/` | Presupuesto, responsabilidad y transparencia fiscal (Ley 819 de 2003) | From its entry into force (9 July 2003, art. 28) to today |
| `endeudamiento-territorial/` | Endeudamiento territorial (Ley 358 de 1997) | From its entry into force (4 February 1997, art. 18) to today |
| `banco-de-la-republica/` | Banco de la República (Ley 31 de 1992) | From its entry into force (4 January 1993, art. 66) to today |
| `seguridad-vial/` | Formación de hábitos de seguridad vial (Ley 1503 de 2011) | From its entry into force (30 December 2011, art. 25) to today |
| `codigo-nacional-de-navegacion-fluvial/` | Código Nacional de Navegación y Actividades Portuarias Fluviales (Ley 1242 de 2008) | From its entry into force (5 August 2008, art. 88) to today |
| `uso-eficiente-del-agua/` | Uso eficiente y ahorro del agua (Ley 373 de 1997) | From its entry into force (6 June 1997, art. 18) to today |
| `residuos-peligrosos/` | Residuos y desechos peligrosos (Ley 1252 de 2008) | From its entry into force (27 November 2008, art. 18) to today |
| `carbono-neutralidad/` | Desarrollo bajo en carbono y carbono neutralidad (Ley 2169 de 2021) | From its entry into force (22 December 2021, art. 38) to today |
| `eliminacion-del-mercurio/` | Uso y reducción del mercurio en actividades industriales (Ley 1658 de 2013) | From its entry into force (15 July 2013, art. 15) to today |
| `agencia-nacional-de-seguridad-vial/` | Agencia Nacional de Seguridad Vial (Ley 1702 de 2013) | From its entry into force (27 December 2013, art. 24) to today |
| `superintendencia-de-industria-y-comercio-1992/` | Superintendencia de Industria y Comercio y protección de la competencia (Decreto 2153 de 1992) | From its entry into force (31 December 1992, art. 59) to today |
| `ley-general-de-archivos/` | Ley General de Archivos (Ley 594 de 2000) | From its entry into force (20 July 2000, art. 52) to today |
| `nacionalidad/` | Nacionalidad colombiana (Ley 2332 de 2023) | From its entry into force (25 September 2023, art. 55) to today |
| `politica-integral-migratoria/` | Política Integral Migratoria (Ley 2136 de 2021) | From its entry into force (4 August 2021, art. 91) to today |
| `servicio-de-reclutamiento/` | Servicio de reclutamiento, control de reservas y movilización (Ley 1861 de 2017) | From its entry into force (4 August 2017, art. 81) to today |
| `sistema-general-de-riesgos-profesionales/` | Sistema General de Riesgos Profesionales (Decreto Ley 1295 de 1994) | From its entry into force (24 June 1994, art. 98) to today |
| `prestaciones-riesgos-profesionales/` | Prestaciones del Sistema General de Riesgos Profesionales (Ley 776 de 2002) | From its entry into force (17 December 2002, art. 23) to today |
| `mujer-cabeza-de-familia/` | Mujer cabeza de familia (Ley 82 de 1993) | From its entry into force (3 November 1993, art. 23) to today |
| `registro-de-deudores-alimentarios-morosos/` | Registro de Deudores Alimentarios Morosos (Ley Estatutaria 2097 de 2021) | From its entry into force (2 July 2021, art. 11) to today |
| `feminicidio/` | Feminicidio como delito autónomo (Ley 1761 de 2015, Rosa Elvira Cely) | From its entry into force (6 July 2015, art. 13) to today |
| `unidad-de-informacion-y-analisis-financiero/` | Unidad de Información y Análisis Financiero (Ley 526 de 1999) | From its entry into force (15 August 1999, art. 14) to today |
| `financiacion-del-terrorismo/` | Prevención y sanción de la financiación del terrorismo (Ley 1121 de 2006) | From its entry into force (30 December 2006, art. 28) to today |
| `ley-anticontrabando/` | Contrabando, lavado de activos y evasión fiscal (Ley 1762 de 2015) | From its entry into force (6 July 2015, art. 56) to today |
| `sistema-general-de-participaciones-2007/` | Sistema General de Participaciones (Ley 1176 de 2007) | From its entry into force (1 January 2008, art. 36) to today; the parágrafos Decreto Legislativo 228 de 2026 added until the end of 2026 lapse on 1 January 2027 (on `futuro`) |
| `derecho-de-autor-2018/` | Derecho de autor y derechos conexos (Ley 1915 de 2018) | From its entry into force (12 July 2018, art. 37) to today |
| `racionalizacion-de-tramites-2005/` | Racionalización de trámites y procedimientos administrativos (Ley 962 de 2005) | From its entry into force (8 July 2005, art. 86) to today |
| `ley-antitramites/` | Supresión y reforma de regulaciones, procedimientos y trámites innecesarios (Decreto Ley 19 de 2012) | From its entry into force (10 January 2012, art. 238) to today |
| `sistema-nacional-de-migraciones/` | Sistema Nacional de Migraciones (Ley 1465 de 2011) | From its entry into force (30 June 2011, art. 9) to today |
| `operacion-del-sistema-de-salud/` | Operación del Sistema General de Seguridad Social en Salud (Ley 1797 de 2016) | From its entry into force (13 July 2016, art. 28) to today |
| `rentas-para-la-salud/` | Rentas de destinación específica para la salud (Ley 1393 de 2010) | From its entry into force (12 July 2010, art. 41) to today |
| `plan-nacional-de-desarrollo-2022-2026/` | Plan Nacional de Desarrollo 2022-2026 (Ley 2294 de 2023) | From its entry into force (19 May 2023, art. 372) to today; arts. 336 and 337, struck by Sentencia C-116-26 with effect from 1 January 2027, leave on that day (on `futuro`) |
| `derecho-de-peticion/` | Derecho fundamental de petición (Ley 1755 de 2015) | From its entry into force (30 June 2015, art. 2) to today |
| `reforma-laboral-2025/` | Reforma laboral (Ley 2466 de 2025) | From its entry into force (25 June 2025, art. 70) to today; arts. 24 to 30 (delivery-platform work) take effect twelve months after regulations the source does not date (art. 67), so they are not in the files yet |
| `plan-nacional-de-desarrollo-2018-2022/` | Plan Nacional de Desarrollo 2018-2022 (Ley 1955 de 2019) | From its entry into force (25 May 2019, art. 336) to today; arts. 18, 193, 244 and 314, struck by the Constitutional Court, leave when each ruling took effect (2020 to 2023) |
| `reforma-pensional-2024/` | Sistema de Protección Social Integral para la Vejez, Invalidez y Muerte (Ley 2381 de 2024) | From its sanction (16 July 2024, art. 95) to today, holding only art. 12's parágrafo transitorio and arts. 76, 94 and 95: the Constitutional Court suspended the rest (Auto A-841-25), and Sentencia C-264-26 puts it in force on 1 April 2027 (on `futuro`), less the provisions it returned to the Cámara (arts. 63 inciso 2, 84 numeral 5, 92 inciso 1, 93) |
| `reduccion-de-la-jornada-laboral/` | Reducción de la jornada laboral (Ley 2101 de 2021) | From its entry into force (15 July 2021, art. 8) to today |
| `desconexion-laboral/` | Ley de Desconexión Laboral (Ley 2191 de 2022) | From its entry into force (6 January 2022, art. 8) to today |
| `acoso-sexual-laboral-y-educacion-superior/` | Acoso sexual en el ámbito laboral y en las instituciones de educación superior (Ley 2365 de 2024) | From its entry into force (20 June 2024, art. 24) to today |
| `licencia-de-paternidad-y-parental/` | Licencia de paternidad y licencias parentales (Ley 2114 de 2021) | From its entry into force (29 July 2021, art. 6) to today |
| `primera-infancia-licencia-de-maternidad/` | Atención y cuidado de la primera infancia y licencia de maternidad (Ley 1822 de 2017) | From its entry into force (4 January 2017, art. 3) to today |
| `reforma-del-cpaca-2021/` | Reforma del Código de Procedimiento Administrativo y de lo Contencioso Administrativo (Ley 2080 de 2021) | From its entry into force (25 January 2021, art. 86) to today |
| `reforma-de-la-contratacion-publica-2018/` | Fortalecimiento de la contratación pública (Ley 1882 de 2018) | From its entry into force (15 January 2018, art. 21) to today; art. 12 as printed throughout (the temporary terms of Decreto Legislativo 575 de 2020 during the health emergency are not shown) |
| `reforma-del-codigo-penitenciario-2014/` | Reforma del Código Penitenciario y Carcelario (Ley 1709 de 2014) | From its entry into force (20 January 2014, art. 107) to today |
| `seguridad-ciudadana/` | Seguridad ciudadana (Ley 2197 de 2022) | From its entry into force (25 January 2022, art. 69) to today; the printing errors Decreto 207 de 2022 corrected are in the text until that decree (8 February 2022) |
| `reforma-tributaria-2022/` | Reforma tributaria para la igualdad y la justicia social (Ley 2277 de 2022) | From its entry into force (13 December 2022, art. 96) to today; art. 68, struck by Sentencia C-072-25 with effect deferred to 20 June 2026, leaves on 21 June 2026 |
| `ley-de-inversion-social/` | Ley de Inversión Social (Ley 2155 de 2021) | From its entry into force (14 September 2021, art. 65) to today |
| `ley-de-crecimiento-economico/` | Ley de Crecimiento Económico (Ley 2010 de 2019) | From its entry into force (27 December 2019, art. 160) to today |
| `reforma-tributaria-estructural-2016/` | Reforma tributaria estructural (Ley 1819 de 2016) | From its entry into force (29 December 2016, art. 376) to today |
| `ley-de-financiamiento-2018/` | Ley de Financiamiento (Ley 1943 de 2018) | From its entry into force (28 December 2018, art. 122; art. 70 from 1 July 2019) to 1 January 2020, when Sentencia C-481-19's ruling striking it as a whole took effect; the folder is empty from then |

Where a code's own vigencia article starts different parts on different days, its first commit is dated from the earliest of them and its note quotes the article. One change has no day in any source: Ley 44 de 1981 (Código de Comercio art. 159) is shown on 31 December 1981, the latest day it can have been sanctioned.

The acts come from separate parts of the same build (`corpus.d/`), each checked against today's text on the source before it reached `main`. Where the source gives no text for a provision in some period (most often the 1989 and 1993 wording of articles of the Estatuto Tributario and the Estatuto Orgánico del Sistema Financiero later rewritten), the file reads "[La fuente no da el texto vigente en esta fecha.]" for that period.

**The Código Penal's penalties after 2005.** Ley 890 de 2004, art. 14, raised every penalty of the Parte Especial by a third in the minimum and a half in the maximum, from 1 January 2005, without rewriting the articles. The source prints each article with the raised figures ("con las penas aumentadas") and keeps the earlier wording; this history follows it, so those changes are commits of Ley 890 de 2004 on 1 January 2005. The figures are the publisher's computation of art. 14, as its own warning says. The per-act `README.md` in each folder lists every provision, how often it changed and when.

## A lawyer's questions as git commands

| Question | Command |
| --- | --- |
| What did art. 15 say on 1 January 2004 (under Acto Legislativo 2 de 2003)? | `python tools/en_vigor_el.py 2004-01-01 constitucion 15` |
| The same, with raw git (bash) | `git show $(git rev-list -1 --before="2004-01-01T23:59:59Z" main -- constitucion/art-015.md):constitucion/art-015.md` |
| The same, in PowerShell | `$r = git rev-list -1 --before="2004-01-01T23:59:59Z" main -- constitucion/art-015.md; git show "$($r):constitucion/art-015.md"` |
| Which act or ruling wrote each paragraph of art. 221? | `git blame constitucion/art-221.md` |
| Every change to art. 34, word by word | `git log -p --word-diff constitucion/art-034.md` |
| Every act and ruling in the record, in order | `git log --reverse --format="%ad %an" --date=short main` |
| Everything one act changed | `git show law/al-2-2015` (tags `law/<key>` mark each law's commit) |
| What the Court struck | `git log --author="Sentencia" --format="%ad %an %s" --date=short` |
| The whole Constitution on a date | `python tools/en_vigor_el.py 2000-01-01 constitucion` |

After a rebuild, refresh tags with `git fetch --force --tags`: a plain fetch keeps stale tags.

## Source

The text and every date come from the **Secretaría General del Senado**'s "basedoc" collection ([secretariasenado.gov.co/senado/basedoc](http://www.secretariasenado.gov.co/senado/basedoc/constitucion_politica_1991.html)), compiled by Avance Jurídico and updated to 15 October 2026 (Diario Oficial No. 53.651). It is the only free official site that keeps, for each provision, the earlier texts ("Legislación Anterior": "Texto original de la Constitución Política", "Texto modificado por el Acto Legislativo 2 de 2003"), notes naming the act that changed it with its Diario Oficial date ("Notas de Vigencia"), and the Constitutional Court rulings on it ("Jurisprudencia Vigencia").

The source has **no dated snapshots**. Each version here is rebuilt from those earlier texts and from the source's inline amendment markers ("<Inciso adicionado por el artículo 1 del Acto Legislativo 1 de 2005 ...>"). Today's text in the repository was checked against the source's current text, provision by provision, on 28 October 2026: all 496 provisions match (`tools/verify.py`).

## Dates

- Each commit is dated at **noon, America/Bogota, on the day the change took effect**. Enactment and publication dates are trailers (`Enacted:`, `Published:`); the in-force day is in `In-force:`, which the tools read.
- **Actos Legislativos** take effect on the day of their publication in the Diario Oficial, as the source's notes say ("Rige a partir de su publicación"), unless the note quotes another vigencia clause: Acto Legislativo 1 de 2001 from 1 January 2002; Actos Legislativos 1 and 4 de 2007 from 1 January 2008; and the clauses tied to elections, Acto Legislativo 2 de 2005 (12 March 2006), 3 de 2005 (14 March 2010) and 3 de 2007 (28 October 2007). The election days come from the Registraduría Nacional del Estado Civil, read from pages by Lexifina's code: its [Calendario Electoral 2006 - 2010](https://www.registraduria.gov.co/Calendario-Electoral-2006-2010.html) (Resolución 0497 de 2005), its [Comunicado de Prensa No. 050 de 2009](https://web.archive.org/web/20110726040247id_/http://www.registraduria.gov.co/ESTA-LISTO-EL-PRE-CALENDARIO.html) (Internet Archive copy), and its [home page of 30 September 2007](https://web.archive.org/web/20070930160642id_/http://www.registraduria.gov.co/) ("el proceso electoral del 28 de octubre"; the year is the capture's). Each of those commits names its source in the message.
- **Default rule** for ordinary laws: Ley 4 de 1913 (Código de Régimen Político y Municipal), arts. 52 and 53: a law binds two months after promulgation unless it fixes its own date.
- **The Constitution of 1991** took effect on its promulgation (art. 380), in Gaceta Constitucional No. 114 of 4 July 1991. The source gives the text of the second corrected edition (Gaceta No. 116 of 20 July 1991), which is the first commit; the corrections of the Aclaración published in Gaceta No. 125 (25 September 1991) are a commit of their own.
- **Court rulings** (Corte Constitucional) are dated by the day of the ruling, as the source gives it.
- `--before="YYYY-MM-DD"` alone uses your clock's time of day, so a change that took effect that day may be missed before noon. Use `T23:59:59Z` as above, or the tool.

## What "author" means

The author of a commit is the act or ruling that made the change, with an e-mail address that cannot exist (`al-2-2015@secretariasenado.invalid`), so `git blame` and `git log --author` name them. The committer is always Lexifina.

- **Credits come only from the source.** A change is credited to an Acto Legislativo only when the source's earlier texts, markers or notes name it.
- **Constitutional Court rulings are authors too** (kind `court`). When the Court struck a whole Acto Legislativo (for example Sentencia C-816 de 2004 on Acto Legislativo 2 de 2003, C-740 de 2013 on Acto Legislativo 2 de 2012, C-294 de 2021 on Acto Legislativo 1 de 2020), the provision returns, on the ruling's day, to its text before that act. When it struck words ("<Aparte tachado INEXEQUIBLE>"), the struck words are in the text until the ruling and gone after it.
- Blame credits whole lines (one paragraph per line). Use `git log -p --word-diff` to see exactly which words each act changed.

## What it does not show

- **Gaps in the source.** For a few provisions the source names an act that changed them but gives no text for the period after it (a later act rewrote the same words, and only the latest text is kept). There the file reads `[La fuente no da el texto vigente en esta fecha.]` for that period, credited to the act named; nothing is guessed. The cases (arts. 122, 256, 263, 322, 328 and 361) are listed in `REPRODUCE.md`. Art. 263 also holds the text of the former art. 263-A, which Acto Legislativo 2 de 2015 moved there.
- **Rulings that change no words.** Plain EXEQUIBLE rulings, inhibitions and "estarse a lo resuelto" rulings are not recorded.
- **Avance Jurídico's editorial notes**, concordances and commentary are not in the text; the notes are used only to date and credit changes.
- **The first printing** of the Constitution (Gaceta No. 114) is not in the source; the history starts with the corrected text of Gaceta No. 116.

## How it is built

Lexifina reads the sources listed here and records each act's dated versions, and the laws that made each change, in one corpus file. `tools/build.py` writes this repository from that file, and the same corpus always gives the same commit hashes; `REPRODUCE.md` gives the details and the checks. A model (Claude) wrote Lexifina's code; it wrote no legal text, and no model runs when the history is built.

No AI model wrote or changed legal text. Claude Opus 5.5 wrote the scripts and chose the sources; see `REPRODUCE.md`.

## Sources

| Source | Kind | Past versions | Names the amending act | Bulk | Notes |
| --- | --- | --- | --- | --- | --- |
| [Secretaría General del Senado, basedoc](http://www.secretariasenado.gov.co/senado/basedoc/) | Official legislation (compiled by Avance Jurídico) | earlier texts per provision, no dated snapshots | yes, per provision, with Diario Oficial dates and Court rulings | per document (HTML pages plus one JavaScript file per page holding the note boxes) | Used |
| [SUIN-Juriscol](https://www.suin-juriscol.gov.co) (Ministerio de Justicia) | Official legislation | no dated versions seen | yes ("Adicionado por: Art. 2 Ley 1482 de 2011"), with Court rulings attached | no | An Angular app that serves no text to a plain request; it does not keep earlier texts. Not used |
| [Registraduría Nacional del Estado Civil](https://www.registraduria.gov.co) | Electoral authority | n/a | n/a | no | Used only for the days of three elections that Actos Legislativos take effect on (two pages through Internet Archive captures pinned by timestamp) |
| Diario Oficial (Imprenta Nacional) | Official gazette | n/a | n/a | no | Not read; the source gives the Diario Oficial number and date of every act |

Research guides that cover every country: [GlobaLex](https://www.nyulawglobal.org/globalex/) and the [Law Library of Congress Guide to Law Online](https://www.loc.gov/research-centers/law-library-of-congress/researcher-resources/guide-to-law-online/).

## Licence

The Constitution, laws and judicial decisions of Colombia may be reproduced freely (Ley 23 de 1982, art. 41), provided the official text is reproduced faithfully. Fuente: Secretaría General del Senado de la República, www.secretariasenado.gov.co. The arrangement, tables, commit messages and tools are by Lexifina, under the terms in `LICENSE`.

This repository is not legal advice and not an official publication.

## En español

Historia del derecho colombiano en git: un archivo por disposición y un commit por acto o sentencia, fechado el día de su entrada en vigencia y firmado por el acto legislativo o la sentencia de la Corte Constitucional que hizo el cambio (`git blame` nombra la norma de cada párrafo). Contiene la Constitución Política de 1991 desde su promulgación el 4 de julio de 1991, con todos sus Actos Legislativos y las sentencias que los declararon inexequibles, y los códigos y leyes de la tabla de arriba (entre ellos el Código Civil, el Código Penal, el Código General del Proceso, el CPACA, el Estatuto Tributario, la Ley 80 de 1993, el Estatuto del Consumidor, el Código Nacional de Tránsito, el Estatuto Orgánico del Sistema Financiero, el Código de Minas, los dos Códigos Procesales del Trabajo (Decreto-Ley 2158 de 1948, derogado desde el 2 de abril de 2026, y Ley 2452 de 2025), la Ley 1116 de 2006, la Ley 142 de 1994, la Ley 1150 de 2007, el Estatuto Anticorrupción, la Ley de Transparencia, la Ley 789 de 2002, la Ley 1429 de 2010, la Ley 1523 de 2012, la Ley General Ambiental, la Ley 388 de 1997, el Código Nacional de Recursos Naturales Renovables, la Ley Estatutaria de la Administración de Justicia, el Código Disciplinario Único (derogado desde el 29 de marzo de 2022), el Código Penitenciario y Carcelario, la Ley de Víctimas y Restitución de Tierras, la Ley General de Educación, la Ley 30 de 1992, la Ley 136 de 1994, la Ley 1258 de 2008, la Ley 1266 de 2008, la Ley 527 de 1999, el Reglamento del Congreso (Ley 5 de 1992), el Decreto 2591 de 1991 (acción de tutela), la Ley 472 de 1998 (acciones populares y de grupo), la Ley 393 de 1997 (acción de cumplimiento), el Código Disciplinario del Abogado, el Código de Extinción de Dominio, el Estatuto de Arbitraje, el Estatuto de Conciliación, el Código de Procedimiento Penal de 2000 (Ley 600 de 2000), la Ley 610 de 2000, la Ley 134 de 1994, la Ley 489 de 1998, la Ley 909 de 2004, la Ley Orgánica del Plan de Desarrollo, la Ley Orgánica de Ordenamiento Territorial, la Ley 617 de 2000, la Ley 715 de 2001, la Ley 42 de 1993, la Ley 1757 de 2015, el Estatuto Orgánico del Presupuesto (Decreto 111 de 1996), el Estatuto Orgánico de Bogotá (Decreto 1421 de 1993), la Ley 1340 de 2009 (protección de la competencia), la Ley 256 de 1996 (competencia desleal), la Ley 1341 de 2009 (TIC), la Ley Estatutaria de Salud, la Ley 1438 de 2011, la Ley 1257 de 2008, la Ley 1010 de 2006 (acoso laboral), la Ley 1562 de 2012 (riesgos laborales), la Ley 1676 de 2013 (garantías mobiliarias), la Ley 160 de 1994 (reforma agraria), la Ley 1508 de 2012 (asociaciones público privadas), la Ley 1682 de 2013 (infraestructura de transporte), la Ley 1778 de 2016 (soborno transnacional), la Ley 1333 de 2009 (procedimiento sancionatorio ambiental), la Ley General de Cultura, la Ley del Deporte, la Ley General de Turismo, la Ley 1122 de 2007, la Ley 1618 de 2013, la Ley 1996 de 2019, la Ley 294 de 1996 (violencia intrafamiliar), la Ley 1146 de 2007, la Ley 1251 de 2008 (adultos mayores), la Ley 1361 de 2009 (protección integral a la familia), el Estatuto de Ciudadanía Juvenil, la Ley 2213 de 2022, la Ley 1066 de 2006, la Ley 1551 de 2012, la Ley 1625 de 2013 (áreas metropolitanas), la Ley 2200 de 2022 (régimen departamental), la Ley 675 de 2001 (propiedad horizontal), la Ley 820 de 2003 (arrendamiento de vivienda urbana), el Estatuto de Registro de Instrumentos Públicos (Ley 1579 de 2012), la Ley 546 de 1999, la Ley 1537 de 2012, la Ley 143 de 1994 (eléctrica), la Ley 1715 de 2014 (energías renovables), la Ley 1931 de 2018 (cambio climático), la Ley 1306 de 2009, la Ley 105 de 1993 y la Ley 336 de 1996 (transporte), el Código Sanitario Nacional (Ley 9 de 1979), el Código de Régimen Municipal (Decreto 1333 de 1986), la Ley 130 de 1994 y la Ley 1475 de 2011 (partidos), la Ley de Garantías Electorales, la Ley 163 de 1994, el Estatuto de la Oposición, la Ley 850 de 2003 (veedurías ciudadanas), la Ley 590 de 2000 (mipymes), la Ley 2069 de 2020 y la Ley 1014 de 2006 (emprendimiento), la Ley 4 de 1992, la Ley 2056 de 2020 (regalías), la Ley 361 de 1997, la Ley 1221 de 2008 (teletrabajo), la Ley 2088 de 2021 (trabajo en casa), la Ley 2121 de 2021 (trabajo remoto), la Ley de Salud Mental, la Ley 2195 de 2022, la Ley 2052 de 2020, la Ley 2014 de 2019, la Ley 1145 de 2007, la Ley 1328 de 2009 (consumidor financiero), la Ley 964 de 2005 (mercado de valores), la Ley 797 de 2003 (pensiones), la Ley 1231 de 2008 (factura), la Ley 1735 de 2014, la Ley 1870 de 2017, la Ley 510 de 1999, la Ley 101 de 1993 (desarrollo agropecuario), la Ley 1776 de 2016 (Zidres), el Código Penal Militar, el Código Disciplinario Militar, el Régimen Disciplinario de la Policía Nacional, la Ley 1095 de 2006 (hábeas corpus), la Ley 137 de 1994 (estados de excepción), la Ley 1621 de 2013 (inteligencia), la Ley 418 de 1997 (orden público), la Ley 975 de 2005 (justicia y paz) las Leyes 1957 de 2019 y 1922 de 2018 (Jurisdicción Especial para la Paz), y las leyes de educación, ciencia y cultura de la tabla (Leyes 1324 de 2009, 1188 de 2008, 749 de 2002, 1286 de 2009, 1951 de 2019, 1740 de 2014, 1620 de 2013, 1064 de 2006, 1493 de 2011 y 1834 de 2017), y las leyes de salud de la tabla (Leyes 1384 de 2010, 1733 de 2014, 1335 de 2009, 1566 de 2012, 1355 de 2009, 1392 de 2010, 972 de 2005, 1805 de 2016, 1164 de 2007 y 1414 de 2010), y las leyes de administración pública, profesiones y otras materias de la tabla (Leyes 190 de 1995, 87 de 1993, 1820 de 2016, 1314 de 2009, 842 de 2003, 1636 de 2013, 44 de 1993, 400 de 1997, 1527 de 2012 y 1828 de 2017), y los códigos derogados de la tabla, hasta su derogación (el Código Contencioso Administrativo de 1984, el Código Nacional de Policía de 1970, el Código del Menor de 1989, el Código de Procedimiento Civil de 1970 y, hasta la Ley 2200 de 2022, el Código de Régimen Departamental de 1986), y las leyes sociales y de vivienda de la tabla (Leyes 1090 de 2006, 1780 de 2016, 1228 de 2008, 1796 de 2016, 2079 de 2021, 131 de 1994, 985 de 2005, 2126 de 2021, 1804 de 2016 y 1641 de 2013), y las leyes de igualdad, minorías, desplazamiento y servicios de la tabla (Leyes 70 de 1993, 387 de 1997, 581 de 2000, 823 de 2003, 1496 de 2011, 1413 de 2010, 731 de 2002, 119 de 1994, 1369 de 2009 y 2166 de 2021), y las leyes de distritos, comunicaciones y salud de la tabla (Leyes 1700 de 2013, 1617 de 2013, 768 de 2002, 182 de 1995, 2015 de 2020, 1419 de 2010 y 1287 de 2009) y, hasta su derogación, las Leyes 743 de 2002 y 375 de 1997, y las leyes de hacienda pública, control fiscal, transporte y ambiente de la tabla (Decreto Ley 403 de 2020 y Leyes 819 de 2003, 358 de 1997, 31 de 1992, 1503 de 2011, 1242 de 2008, 373 de 1997, 1252 de 2008, 2169 de 2021, 1658 de 2013 y 1702 de 2013), y las leyes de competencia, archivos, nacionalidad, migración y servicio militar de la tabla (Decreto 2153 de 1992 y Leyes 594 de 2000, 2332 de 2023, 2136 de 2021 y 1861 de 2017), y las leyes de riesgos laborales, mujer y familia de la tabla (Decreto Ley 1295 de 1994 y Leyes 776 de 2002, 82 de 1993, 2097 de 2021 y 1761 de 2015), y las leyes de inteligencia financiera, contrabando, participaciones y derecho de autor de la tabla (Leyes 526 de 1999, 1121 de 2006, 1762 de 2015, 1176 de 2007 y 1915 de 2018), y las leyes antitrámites y de migraciones de la tabla (Ley 962 de 2005, Decreto Ley 19 de 2012 y Ley 1465 de 2011), y las leyes de salud y el Plan Nacional de Desarrollo de la tabla (Leyes 1797 de 2016, 1393 de 2010 y 2294 de 2023), y la ley de derecho de petición, la reforma laboral de 2025 y el Plan Nacional de Desarrollo 2018-2022 de la tabla (Leyes 1755 de 2015, 2466 de 2025 y 1955 de 2019), y la reforma pensional de la tabla (Ley 2381 de 2024, que rige en su mayor parte desde el 1 de abril de 2027, en la rama futuro), y las leyes laborales de jornada, desconexión, acoso sexual y licencias de la tabla (Leyes 2101 de 2021, 2191 de 2022, 2365 de 2024, 2114 de 2021 y 1822 de 2017), y las reformas del CPACA, de la contratación pública y del Código Penitenciario de la tabla (Leyes 2080 de 2021, 1882 de 2018 y 1709 de 2014), y la ley de seguridad ciudadana de la tabla (Ley 2197 de 2022), y las reformas tributarias de la tabla (Leyes 2277 de 2022, 2155 de 2021 y 2010 de 2019), y la reforma tributaria estructural de la tabla (Ley 1819 de 2016), y, hasta que la Corte Constitucional la declaró inexequible, la Ley de Financiamiento de la tabla (Ley 1943 de 2018, hasta el 1 de enero de 2020)).

- Texto vigente en una fecha: `python tools/en_vigor_el.py 2004-01-01 constitucion 15`
- Fuente: Secretaría General del Senado (basedoc). La fuente no tiene versiones fechadas: cada versión se reconstruye con la "Legislación Anterior", las notas de vigencia y las marcas de modificación de la propia fuente. El texto de hoy coincide con el de la fuente en las 496 disposiciones (28 de octubre de 2026).
- Fechas: los Actos Legislativos rigen desde su publicación en el Diario Oficial, salvo que la nota cite otra regla de vigencia; las sentencias, desde su fecha. Regla supletoria para las leyes: Ley 4 de 1913, arts. 52 y 53.
- Donde la fuente no da el texto de un período, el archivo dice "[La fuente no da el texto vigente en esta fecha.]". Ningún modelo de IA escribió texto legal.
