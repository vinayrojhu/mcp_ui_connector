# Frontend flow

The home screen accepts a task and reports planning status. A plan card displays objective, application, environment, actions, expected result, and risk. A proposed connector card shows the finite action list and offers Run. Execution status is shown in the right panel. The frontend reports backend policy and transport errors accessibly.

The API includes a stored event stream endpoint. This initial screen uses the synchronous execution response and does not yet subscribe to SSE. Approval cards, connector registry pages, and execution detail routes are not part of this MVP slice.
