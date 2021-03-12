# HuaweiCodeCraft2021
- [Official Site](https://competition.huaweicloud.com/advance/1000041380)

# Data Structure
## Attribute
- TrainingData
  - server_type_num, number
  - server_type_list, list<dict>
    - server_name
    - server_cpu_num
    - server_memory_size
    - server_hardware_cost
    - server_energy_cost
  - vm_type_num, number
  - vm_type_list, list<dict>
    - vm_name
    - vm_cpu_num
    - vm_memory_size
    - vm_deployment_way
  - daily_num, number
  - daily_queue_list, list<DailyQueue>

- DailyQueue
  - daily_queue_length, number
  - daily_queue_info, list<dict>
    - request_item_action
    - request_item_vm_type
    - request_item_vm_id

## Get Method
- get_<field_name>()


# Code Convention
## Code Style
- [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

## Git commit message
- feat: The new feature you're adding to a particular application
- fix: A bug fix
- style: Feature and updates related to styling
- refactor: Refactoring a specific section of the codebase
- test: Everything related to testing
- docs: Everything related to documentation
- chore: Regular code maintenance.[ You can also use emojis to represent commit types]

Demo:
```
git commit -m "#fix: value of return error"
```
