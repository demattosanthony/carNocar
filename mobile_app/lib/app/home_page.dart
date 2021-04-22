import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:flutter/material.dart';
import 'package:mobile_app/app/map.dart';
import 'package:mobile_app/app/theme.dart';
import 'package:mobile_app/locator.dart';
import 'package:mobile_app/services/db_service.dart';

class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  @override
  void initState() {
    super.initState();
    sl<DbService>().getSpacesStatus();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: StreamBuilder<QuerySnapshot>(
        stream: sl<DbService>().getSpacesStatus(),
        builder: (ctx, snapshot) {
          if (snapshot.hasData) {
            var openList = snapshot.data.docs
                .where((element) => element['status'] == 'open');
            var numOpen = openList.length;

            return CustomScrollView(
              slivers: [
                SliverAppBar(
                  expandedHeight: MediaQuery.of(context).size.height * .15,
                  collapsedHeight: MediaQuery.of(context).size.height * .10,
                  forceElevated: false,
                  pinned: true,
                  flexibleSpace: FlexibleSpaceBar(
                    title: Container(
                      padding: EdgeInsets.only(left: 10, bottom: 15),
                      child: Text('Couch Parking Lot\nOpen Spots: $numOpen',
                          style: TextStyle(color: Colors.black, fontSize: 22)),
                    ),
                    centerTitle: false,
                    titlePadding: EdgeInsets.all(0),
                  ),
                ),
                SliverToBoxAdapter(
                  child: CustomMap(numOpen),
                ),
                SliverList(
                    delegate: SliverChildBuilderDelegate((ctx, index) {
                  var status = snapshot.data.docs[index]['status'];
                  var spaceId = snapshot.data.docs[index].id;
                  return status == 'open'
                      ? Card(
                          elevation: 0,
                          child: ListTile(
                            leading: CircleAvatar(
                              backgroundColor: Colors.white,
                              backgroundImage:
                                  AssetImage('assets/images/spot_open.png'),
                              radius: 35,
                            ),
                            title: Text(
                              'Space ID: ' + spaceId,
                              style: listTitleStyle,
                            ),
                            subtitle: Padding(
                              padding: const EdgeInsets.all(8.0),
                              child: Text(
                                'Status: ' + status,
                                style: listSubTitleStyle,
                              ),
                            ),
                          ),
                        )
                      : Card(
                          elevation: 0,
                          child: ListTile(
                            leading: CircleAvatar(
                              backgroundColor: Colors.white,
                              backgroundImage:
                                  AssetImage('assets/images/spot_taken.png'),
                              radius: 35,
                            ),
                            title: Text(
                              'Space ID: ' + spaceId,
                              style: listTitleStyle,
                            ),
                            subtitle: Padding(
                              padding: const EdgeInsets.all(8.0),
                              child: Text(
                                'Status: ' + status,
                                style: listSubTitleStyle,
                              ),
                            ),
                          ),
                        );
                }, childCount: snapshot.data.docs.length))
              ],
            );
          } else {
            return Container();
          }
        },
      ),
    );
  }
}
