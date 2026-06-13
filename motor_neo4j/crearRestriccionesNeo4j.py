def crearRestricciones(driver, base_datos):
    try:
        with driver.session(database=base_datos) as session:
            session.run("""
                CREATE CONSTRAINT caballo_id_unico IF NOT EXISTS
                FOR (c:Caballo)
                REQUIRE c.id IS UNIQUE
            """)

            session.run("""
                CREATE CONSTRAINT carrera_id_unico IF NOT EXISTS
                FOR (c:Carrera)
                REQUIRE c.id IS UNIQUE
            """)

            session.run("""
                CREATE CONSTRAINT entrenador_nombre_unico IF NOT EXISTS
                FOR (e:Entrenador)
                REQUIRE e.nombre IS UNIQUE
            """)

            session.run("""
                CREATE CONSTRAINT jockey_nombre_unico IF NOT EXISTS
                FOR (j:Jockey)
                REQUIRE j.nombre IS UNIQUE
            """)

            session.run("""
                CREATE INDEX caballo_nombre_idx IF NOT EXISTS
                FOR (c:Caballo)
                ON (c.nombre)
            """)

        print("Restricciones e índices creados/verificados correctamente en Neo4j.")

    except Exception as e:
        print(f"Error al crear restricciones en Neo4j: {e}")