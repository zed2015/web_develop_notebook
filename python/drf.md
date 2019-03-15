### validate 验证逻辑

#### validate 的顺序
- `to_internal_value`
    - `primitive = field.get_value(initial_data)`
    - `validated_value = field.run_validation(primitive)`
        - `field.validate_empty(primitive)`
    - `validated_value = validate_method(validated_value)`
    - `ret = set_value(validated_value)  `
- `run_validators(ret)`
    - `field.validators(ret)`
- `validate(ret)`

#### partial 生效是以root serializer的partial参数为准


#### `to_internal_value` 之后的值是 `source_attribute` 作为 key 的

#### `attribute = field.get_attribute(instance)` 通过`source_attribute` 来取的

#### `field.to_representation(attribute)` 来展现
