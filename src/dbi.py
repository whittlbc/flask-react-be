"""
Postgres Database Interface With Soft-Destroyable Models
"""
from src import db

IS_DESTROYED = 'is_destroyed'  # column used for soft-destroying models


def find_one(model, params=None, session=None, unscoped=False):
  """
  Find the first record of a database model per specified query params

  :param model:    (required) model class to query (check models.py)
  :param params:   (optional) dict of params to query model with
  :param session:  (optional) database session (if not provided, will be created)
  :param unscoped: (optional) whether to gather ALL query results, regardless of model's is_destroyed status

  :return: first model instance returned from DB query
  """
  params, session = ensure_args(params, session)

  if hasattr(model, IS_DESTROYED) and not params.get(IS_DESTROYED) and not unscoped:
    params[IS_DESTROYED] = False

  return session.query(model).filter_by(**params).first()


def find_all(model, params=None, session=None, unscoped=False):
  """
  Find ALL records of a database model per specified query params

  :param model:    (required) model class to query (check models.py)
  :param params:   (optional) dict of params to query model with
  :param session:  (optional) database session (if not provided, will be created)
  :param unscoped: (optional) whether to gather ALL query results, regardless of model's is_destroyed status

  :return: list of model instances
  """

  params, session = ensure_args(params, session)
  exact_params = {}
  list_params = {}

  for k, v in params.items():
    if type(v).__name__ in ['list', 'tuple']:
      list_params[k] = tuple(v)
    else:
      exact_params[k] = v

  if hasattr(model, IS_DESTROYED) and not exact_params.get(IS_DESTROYED) and not unscoped:
    exact_params[IS_DESTROYED] = False

  query = session.query(model).filter_by(**exact_params)

  for k, v in list_params.items():
    query = query.filter(getattr(model, k).in_(v))

  return query.all()


def find_or_initialize_by(model, find_by_params=None, update_params=None, session=None, unscoped=False):
  """
  Find record for a model if it exists, and if not, create it.

  :param model:           (required) model class to query (check models.py)
  :param find_by_params:  (optional) dict of params to find unique model by
  :param update_params:   (optional) dict of params to update the model with (non-find-by params...not unique)
  :param session:         (optional) database session (if not provided, will be created)
  :param unscoped:        (optional) whether to gather ALL query results, regardless of model's is_destroyed status

  :return: (tuple) -- (model instance, if the record was just created or not)
  """

  find_by_params, session = ensure_args(find_by_params, session)
  record = find_one(model, find_by_params.copy(), session, unscoped)
  update_params = update_params or {}

  if not record:
    is_new = True
    find_by_params.update(update_params)  # merge the 2 dicts
    record = create(model, find_by_params, session)
  else:
    is_new = False
    record = update(record, update_params, session)

  return record, is_new


def update(model_instance, params=None, session=None):
  """
  Find record for a model if it exists, and if not, create it.

  :param model_instance:    (required) model instance to update
  :param params:            (optional) dict of params to update model with
  :param session:           (optional) database session (if not provided, will be created)

  :return: the updated model instance
  """
  params, session = ensure_args(params, session)

  try:
    [setattr(model_instance, k, v) for k, v in params.items()]
    session.commit()
  except Exception as e:
    raise Exception(
      'Error updating {} with params: {} with error: {}'.format(type(model_instance).__name__, params, e.message))

  return model_instance


def create(model, params=None, session=None):
  """
  Create a model and save a new record for specified model class and params

  :param model:     (required) model class to create new record for
  :param params:    (model-dependent) dict of params to create model with
  :param session:   (optional) database session (if not provided, will be created)

  :return: the created model instance
  """
  params, session = ensure_args(params, session)
  model_instance = model(**params)

  try:
    session.add(model_instance)
    session.commit()
  except Exception as e:
    raise Exception('Error creating {} with params: {} with error: {}'.format(model, params, e.message))

  return model_instance


def destroy(model, params=None, session=None):
  """
  Soft-Destroy a model by certain query params

  :param model:    (required) model class to soft-destroy
  :param params:   (optional) params to find model instance with
  :param session:  (optional) database session (if not provided, will be created)

  :return: (boolean) whether the model instance was successfully soft-destroyed
  """
  if not hasattr(model, IS_DESTROYED):
    return delete(model, params, session)

  params, session = ensure_args(params, session)
  result = find_one(model, params, session)

  if result:
    result.is_destroyed = True
    session.commit()
    return True

  return False


def destroy_instance(model_instance, session=None):
  """
  Soft-Destroy a model instance

  :param model_instance:    (required) model instance to soft-destroy
  :param session:           (optional) database session (if not provided, will be created)

  :return: (boolean) whether the model instance was successfully soft-destroyed
  """
  # if model doesn't have an is_destroyed column, delete the instance instead.
  if not hasattr(model_instance, IS_DESTROYED):
    return delete_instance(model_instance, session)

  session = session or create_session()
  model_instance.is_destroyed = True
  session.commit()

  return True


def undestroy(model, params=None, session=None):
  """
  Undestroy a model by certain query params

  :param model:    (required) model class to undestroy
  :param params:   (optional) params to find model instance with
  :param session:  (optional) database session (if not provided, will be created)

  :return: (boolean) whether the model instance was successfully undestroyed
  """
  if not hasattr(model, IS_DESTROYED):
    raise Exception('Can\'t undestroyed a model ({}) without an \'is_destroyed\' column.'.format(model))

  params, session = ensure_args(params, session)
  result = find_one(model, params, session)

  if result:
    try:
      result.is_destroyed = False
      session.commit()
    except Exception as e:
      raise Exception('Error creating {} with params: {} with error: {}'.format(model, params, e.message))

    return True
  else:
    return False


def undestroy_instance(model_instance, session=None):
  """
  Undestroy a model instance

  :param model:    (required) model instance to undestroy
  :param session:  (optional) database session (if not provided, will be created)

  :return: (boolean) whether the model instance was successfully undestroyed
  """
  if not hasattr(model_instance, IS_DESTROYED):
    raise Exception(
      'Can\'t undestroyed a model ({}) without an \'is_destroyed\' column.'.format(type(model_instance).__name__))

  session = session or create_session()
  model_instance.is_destroyed = False
  session.commit()
  return True


def delete(model, params=None, session=None):
  """
  Delete a model by certain query params

  :param model:    (required) model class to delete
  :param params:   (optional) params to find model instance with
  :param session:  (optional) database session (if not provided, will be created)

  :return: (boolean) whether the model instance was successfully deleted
  """
  params, session = ensure_args(params, session)
  result = find_one(model, params, session)

  if result:
    try:
      session.delete(result)
      session.commit()
    except Exception as e:
      raise Exception('Error deleting {} with params: {} with error: {}'.format(model, params, e.message))

    return True
  else:
    return False


def delete_instance(model_instance, session=None):
  """
  Delete a model by certain query params

  :param model_instance:    (required) model instance to delete
  :param session:           (optional) database session (if not provided, will be created)

  :return: (boolean) whether the model instance was successfully deleted
  """
  session = session or create_session()

  try:
    session.delete(model_instance)
    session.commit()
  except Exception as e:
    raise Exception('Error deleting {} with error: {}'.format(type(model_instance).__name__, e.message))

  return True


def create_session():
  return db.session


def ensure_args(params, session):
  params = params or {}
  session = session or create_session()
  return params, session