import cbpos
from cbpos.modules import BaseModuleMetadata

class ModuleMetadata(BaseModuleMetadata):
    base_name = 'auth'
    version = '0.1.0'
    display_name = 'Authentication Module'
    dependencies = (
        ('base', '0.1'),
    )
    config_defaults = (
        ('mod.auth', {
                      'allow_empty_passwords': False,
                      }
         ),
    )
