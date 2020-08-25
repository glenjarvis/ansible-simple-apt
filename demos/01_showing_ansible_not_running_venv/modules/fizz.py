#!/vagrant/tools_venv/bin/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}

DOCUMENTATION = '''
---
module: fizz
short_description: Silly module just to demo Python versions
description:
  - Demonstrates a custom module
version_added: "0.0.2"
options:
  number:
    description:
      - The number for which to respond. If it's divisible by 3 response is Fizz. If it is divisible by 5, Buzz.
        If it is divizible by both, it is FizzBuzz. Otherwise, it is the number itself.
requirements:
   - None
author: "Glen Jarvis (glen@glenjarvis.com)"
notes:
   - This is a toy demo and is not actually functional
'''

EXAMPLES = '''
- name: Fizz
  fizz:
    number: 3

- name: Buzz
  fizz:
    number: 5

- name: FizzBuzz
  fizz:
    number: 15

- name: Any number
  fizz:
    number: 14
'''

RETURN = '''
response:
    description: 
    returned: String describing the number
    type: str
    sample: FizzBuzz
'''

from ansible.module_utils.basic import AnsibleModule

def main():
    module = AnsibleModule(
        argument_spec=dict(
            number=dict(type='int', default=0),
        ),
    )

    num = module.params['number']
    response = num
    if num % 15 == 0:
        response = "FizzBuzz" 
    elif num % 3 == 0:
        response = "Fizz" 
    elif num % 5 == 0:
        response = "Buzz" 

    module.exit_json(response=response)

if __name__ == "__main__":
    main()
