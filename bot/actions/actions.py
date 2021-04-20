# """ from typing import Text, List, Any, Dict

# from rasa_sdk import Tracker, FormValidationAction
# from rasa_sdk.executor import CollectingDispatcher
# from rasa_sdk.types import DomainDict


# class ValidateChatForm(FormValidationAction):
#     def name(self) -> Text:
#         return "validate_chat_form"

#     def validate_pain(
#         self,
#         slot_value: Any,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: DomainDict,
#     ) -> Dict[Text, Any]:
#         """Validate `first_name` value."""

#         # If pain is not a number, it might be wrong.
#         print(f"Pain Score given = {slot_value} type = {type(slot_value)}")
#         if slotvalue.isnumeric():
#             return {"pain": slot_value}
#         else:
#             dispatcher.utter_message(text=f"Please enter a number between 1 and 10")
#             return {"pain": None}
# #Other """