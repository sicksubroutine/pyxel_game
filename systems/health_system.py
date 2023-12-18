import esper as es

from components.health import Health


class HealthSystem(es.Processor):
    def process(self):
        for ent, (health,) in es.get_components(Health):
            if health.hit_invuln > 0:
                health.hit_invuln -= 1
