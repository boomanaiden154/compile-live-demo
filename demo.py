import subprocess

from datasets import load_dataset

bc_dataset = load_dataset('llvm-ml/ComPile', split='train', streaming=True)

bc_dataset_iter = iter(bc_dataset)

OPT_PATH = 'opt'

total_instruction_count = []

for bc_index in range(0,100):
  bc_contents = next(bc_dataset_iter)['content']
  command_vector = ['/tmp/opt', '-passes=print<func-properties>', '-enable-detailed-function-properties', '-', '-disable-output']
  result = subprocess.run(command_vector, input=bc_contents, capture_output=True)
  for line in result.stderr.decode('utf-8').split('\n'):
    if line.startswith('TotalInstructionCount'):
      total_instruction_count.append(int(line.split('TotalInstructionCount: ')[1]))
      break

print(total_instruction_count)

