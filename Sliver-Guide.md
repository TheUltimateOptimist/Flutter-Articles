# Fancy Scrolling using slivers

- ## What is a sliver?
  A sliver is a portion of a scrollable area. Anything that scrolls in Flutter is a sliver. Usually slivers are wrapped in convenience classes like ListView or GridView, because they use a different layout protocol compared to all the other Flutter widgets.

- ## ScrollBehaviour
  The default scroll behaviour is different for each platform as it automatically adapts to present the user with the expected scrolling behaviour. The scroll behaviour informs a scrollable's scrollPhysics and applys decorations like Scrollbars and GlowingOverScrollIndicators

- ## Sliver Layout Protocol
  The sliver layout protocol differs greatly from the box layout protocol. Wheras the box layout protocol uses BoxConstraints to exactly determine a widget's width and height in addition to placing it in a concrete position in the window slivers are layed out using SliverConstraints and SliverGeometry. As a result a sliver can make use of an infinite amount of space in the given axis. Moreover laying out slivers differs greatly from laying out other widgets as now things like width, height or position don't play a role anymore whereas knowing how much of the given sliver is visible, how far off the next sliver is and how far the user has already scrolled is important. With the help of these new information slivers can be built lazily(only slivers that are visible and the ones just over the edge are built).

- ## Lazily building slivers
  A SingleChildScrollView is a single sliver. So if you want to achieve higher efficiency you need to use a widget like ListView.builder which consists of a collection of slivers that are built lazily as they are demanded while scrolling

- ## Manually working with slivers
  - ### Sliver-Wrapper
    When using ListView, GridView, SingleChildScrollView the slivers are abstracted  away for convenience. To control slivers use the CustomScrollView widget.The CustomScrollView then does not take a list of children but a list of slivers.

  - ### Available Slivers
    - #### [SliverList](topics/1/articles/SliverList)
      The SliverList is comparable to the ListView.builder widget. The SliverList takes a SliverChildDelegate that is responsible for providing the displayed children. One kind of SliverChildDelegate is the SliverChildBuilderDelegate which is the same as the builder required by the ListView.builder widget. Similar to ListView.builder the SliverList builds its children lazily as they are starting to become visible on the screen.
    - #### [SliverList](topics/1/articles/SliverAppBar)
      The SliverAppBar share a lot of attributes with the normal AppBar like title, or backGroundColor. But apart from the normal AppBar the SliverAppBar disappears as you scroll and appears again if you scroll back.

- ## Example Code:

      import 'package:flutter/material.dart';

      void main() {
        runApp(HorizonsApp());
      }

      class HorizonsApp extends StatelessWidget {
        // This widget is the root of your application.
        @override
        Widget build(BuildContext context) {
          return MaterialApp(
            debugShowCheckedModeBanner: false,
            // This is the theme of your application.
            theme: ThemeData.dark(),
            scrollBehavior: const ConstantScrollBehavior(),
            title: 'Horizons Weather',
            home: Scaffold(
              body: CustomScrollView(
                slivers: <Widget>[
                  SliverAppBar(
                    pinned: true,
                    stretch: true,
                    onStretchTrigger: () async {
                      print('Load new data!');
                      // await Server.requestNewData();
                    },
                    backgroundColor: Colors.teal[800],
                    expandedHeight: 200.0,
                    flexibleSpace: FlexibleSpaceBar(
                      stretchModes: <StretchMode>[
                        StretchMode.zoomBackground,
                        StretchMode.fadeTitle,
                        StretchMode.blurBackground,
                      ],
                      title: Text('Horizons'),
                      background: DecoratedBox(
                        position: DecorationPosition.foreground,
                        decoration: BoxDecoration(
                          gradient: LinearGradient(
                            begin: Alignment.bottomCenter,
                            end: Alignment.center,
                            colors: <Color>[ Colors.teal[800]!, Colors.transparent ],
                          ),
                        ),
                        child: Image.network(
                          headerImage,
                          fit: BoxFit.cover,
                        ),
                      ),
                    ),
                  ),
                  WeeklyForecastList(),
                ],
              ),
            )
          );
        }
      }

      class WeeklyForecastList extends StatelessWidget {
        @override
        Widget build(BuildContext context) {
          final DateTime currentDate = DateTime.now();
          final TextTheme textTheme = Theme.of(context).textTheme;
          
          return SliverList(
            delegate: SliverChildBuilderDelegate(
              (BuildContext context, int index) {
                final DailyForecast dailyForecast = Server.getDailyForecastByID(index);
                return Card(
                  child: Row(
                    children: <Widget>[
                      SizedBox(
                        height: 200.0,
                        width: 200.0,
                        child: Stack(
                          fit: StackFit.expand,
                          children: <Widget>[
                            DecoratedBox(
                              position: DecorationPosition.foreground,
                              decoration: BoxDecoration(
                                gradient: RadialGradient(
                                  colors: <Color>[ Colors.grey[800]!, Colors.transparent ],
                                ),
                              ),
                              child: Image.network(
                                dailyForecast.imageId,
                                fit: BoxFit.cover,
                              ),
                            ),
                            Center(
                              child: Text(
                                dailyForecast.getDate(currentDate.day).toString(),
                                style: textTheme.headline2,
                              ),
                            ),
                          ],
                        ),
                      ),
                      Expanded(
                        child: Padding(
                          padding: const EdgeInsets.all(20.0),
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: <Widget>[
                              Text(
                                dailyForecast.getWeekday(currentDate.weekday),
                                style: textTheme.headline4,
                              ),
                              SizedBox(height: 10.0),
                              Text(dailyForecast.description),
                            ],
                          ),
                        ),
                      ),
                      Padding(
                        padding: EdgeInsets.all(16.0),
                        child: Text(
                          '${dailyForecast.highTemp} | ${dailyForecast.lowTemp} F',
                          style: textTheme.subtitle1,
                        ),
                      ),
                    ],
                  ),
                );
              },
              childCount: 7,
            ),
          );
        }
      }

      // --------------------------------------------
      // Below this line are helper classes and data.

      const String baseAssetURL = 'https://dartpad-workshops-io2021.web.app/getting_started_with_slivers/';
      const String headerImage = '${baseAssetURL}assets/header.jpeg';

      const Map<int, DailyForecast> _kDummyData = {
        0 : DailyForecast(
          id: 0,
          imageId: '${baseAssetURL}assets/day_0.jpeg',
          highTemp: 73,
          lowTemp: 52,
          description: 'Partly cloudy in the morning, with sun appearing in the afternoon.',
        ),
        1 : DailyForecast(
          id: 1,
          imageId: '${baseAssetURL}assets/day_1.jpeg',
          highTemp: 70,
          lowTemp: 50,
          description: 'Partly sunny.',
        ),
        2 : DailyForecast(
          id: 2,
          imageId: '${baseAssetURL}assets/day_2.jpeg',
          highTemp: 71,
          lowTemp: 55,
          description: 'Party cloudy.',
        ),
        3 : DailyForecast(
          id: 3,
          imageId: '${baseAssetURL}assets/day_3.jpeg',
          highTemp: 74,
          lowTemp: 60,
          description: 'Thunderstorms in the evening.',
        ),
        4 : DailyForecast(
          id: 4,
          imageId: '${baseAssetURL}assets/day_4.jpeg',
          highTemp: 67,
          lowTemp: 60,
          description: 'Severe thunderstorm warning.',
        ),
        5 : DailyForecast(
          id: 5,
          imageId: '${baseAssetURL}assets/day_5.jpeg',
          highTemp: 73,
          lowTemp: 57,
          description: 'Cloudy with showers in the morning.',
        ),
        6 : DailyForecast(
          id: 6,
          imageId: '${baseAssetURL}assets/day_6.jpeg',
          highTemp: 75,
          lowTemp: 58,
          description: 'Sun throughout the day.',
        ),
      };

      class Server {
        static List<DailyForecast> getDailyForecastList() => _kDummyData.values.toList();

        static DailyForecast getDailyForecastByID(int id) {
          assert(id >= 0 && id <= 6);
          return _kDummyData[id]!;
        }
      }

      class DailyForecast {
        const DailyForecast({
          required this.id,
          required this.imageId,
          required this.highTemp,
          required this.lowTemp,
          required this.description,
        });
        final int id;
        final String imageId;
        final int highTemp;
        final int lowTemp;
        final String description;

        static const List<String> _weekdays = <String>[
          'Monday',
          'Tuesday',
          'Wednesday',
          'Thursday',
          'Friday',
          'Saturday',
          'Sunday',
        ];

        String getWeekday(int today) {
          final int offset = today + id;
          final int day = offset >= 7 ? offset - 7 : offset;
          return _weekdays[day];
        }

        int getDate(int today) => today + id;
      }

      class ConstantScrollBehavior extends ScrollBehavior {
        const ConstantScrollBehavior();

        @override
        Widget buildScrollbar(BuildContext context, Widget child, ScrollableDetails details) => child;

        @override
        Widget buildOverscrollIndicator(BuildContext context, Widget child, ScrollableDetails details) => child;

        @override
        TargetPlatform getPlatform(BuildContext context) => TargetPlatform.macOS;

        @override
        ScrollPhysics getScrollPhysics(BuildContext context) => const BouncingScrollPhysics(parent: AlwaysScrollableScrollPhysics());
      }

