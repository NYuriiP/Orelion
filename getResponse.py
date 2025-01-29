from lbl import lbl, TEXT_SPEED
import os

def getResponse(prompt, options: list[str]):
  lbl(f"{prompt}\n\n", "clear", TEXT_SPEED, "")
  for idx, option in enumerate(options):
    lbl(f"{idx + 1} - {option} \n", "clear", 0.05, "")
  print("\n")
  choice = input("Which is your response? \n")
  # we cast to int which can throw error, so we catch
  # it in except clause below also throw if answer is
  # not in the list
  try:
    if (int(choice) > len(options)):
      raise ValueError()
  except ValueError:
    print("Invalid choice\n\n")
    return getResponse(prompt, options)

  os.system('clear')

  return choice
