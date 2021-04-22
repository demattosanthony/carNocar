import 'package:get_it/get_it.dart';
import 'package:mobile_app/services/db_service.dart';

GetIt sl = GetIt.instance;

void setupLocator() {
  //services
  sl.registerLazySingleton(() => DbService());
}
