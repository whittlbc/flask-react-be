"""
Postgres Database Interface providing the following helper methods:

  find_one
  find_all
  update
  create
  destroy
  undestroy
  delete

  * Destroy-ing is the same as "soft" deleting a record...it will simply set the is_destroyed column to True
  for a record. The helper methods used for querying the DB are automatically scoped to include is_destroyed=False
  for a given query. One can simply pass in unscoped=True to these query helper methods to find ALL records for a model,
  regardless of is_destroyed status. NOTE: If a table does NOT have an is_destroyed column on it, calling destroy
  is the same as calling delete, and the record will be completely removed from the database.
  
Usage Examples:

  user = dbi.create(User, {'email': 'my_email@email.com'})

  dbi.update(user, {'email': 'my_updated_email@email.com'})

  dbi.destroy(user)

"""
from src import db

# Column used for soft-deleting models
IS_DESTROYED = 'is_destroyed'


def find_one(model, params={}, unscoped=False):
  """
  Find the first record of a database model per specified query params

  :param model:    (required) model class to query (check models.py)
  :param params:   (optional) dict of params to query model with
  :param unscoped: (optional) whether to gather ALL query results, regardless of model's is_destroyed status

  :return: first model instance returned from DB query
  """
  if hasattr(model, IS_DESTROYED) and not params.get(IS_DESTROYED) and not unscoped:
    params[IS_DESTROYED] = False

  return db.session.query(model).filter_by(**params).first()


def find_all(model, params={}, unscoped=False):
  """
  Find ALL records of a database model per specified query params

  :param model:    (required) model class to query (check models.py)
  :param params:   (optional) dict of params to query model with
  :param unscoped: (optional) whether to gather ALL query results, regardless of model's is_destroyed status

  :return: list of model instances
  """
  exact_params = {}
  list_params = {}

  for k, v in params.items():
    if type(v).__name__ in ['list', 'tuple']:
      list_params[k] = tuple(v)
    else:
      exact_params[k] = v

  if hasattr(model, IS_DESTROYED) and not exact_params.get(IS_DESTROYED) and not unscoped:
    exact_params[IS_DESTROYED] = False

  query = db.session.query(model).filter_by(**exact_params)

  for k, v in list_params.items():
    query = query.filter(getattr(model, k).in_(v))

  return query.all()


def update(model_instance, params={}):
  """
  Update a model instance with new params

  :param model_instance:    (required) model instance to update
  :param params:            (optional) dict of params to update model with

  :return: the updated model instance
  """
  [setattr(model_instance, k, v) for k, v in params.items()]
  db.session.commit()

  return model_instance


def create(model, params={}):
  """
  Create a model and save a new record for specified model class and params

  :param model:     (required) model class to create new record for
  :param params:    (model-dependent) dict of params to create model with

  :return: the created model instance
  """
  model_instance = model(**params)

  db.session.add(model_instance)
  db.session.commit()

  return model_instance


def destroy(model_instance):
  """
  "Soft" delete a model instance (if allowed); otherwise, hard delete it.

  :param model_instance:    (required) model instance to soft delete

  :return: (boolean) whether the model instance was successfully soft deleted
  """
  # If model is not soft-deletable, hard delete it.
  if not hasattr(model_instance, IS_DESTROYED):
    return delete(model_instance)

  model_instance.is_destroyed = True
  db.session.commit()

  return True


def undestroy(model_instance):
  """
  Undestroy a model instance

  :param model:    (required) model instance to undestroy

  :return: (boolean) whether the model instance was successfully undestroyed
  """
  if not hasattr(model_instance, IS_DESTROYED):
    return False

  model_instance.is_destroyed = False
  db.session.commit()

  return True


def delete(model_instance):
  """
  Hard delete a model instance

  :param model_instance:    (required) model instance to hard delete

  :return: (boolean) whether the model instance was successfully hard deleted
  """
  db.session.delete(model_instance)
  db.session.commit()

  return True